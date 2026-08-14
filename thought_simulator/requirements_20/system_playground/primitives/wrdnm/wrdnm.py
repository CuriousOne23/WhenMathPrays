"""
WrdNm — Word-to-Numeric Encoder (Version 1.0)
Path-A pure numeric encoding primitive for ISc.

Responsibilities:
  1. Load wrdnm_schema.yaml + dictionaries + scalar tables + hash_config
  2. Read structured TP fields via nested paths declared in the schema
  3. Convert: categorical → float32 ID, boolean → 0/1, scalar → float32, hashed → uint32
  4. Assemble numeric feature vector in canonical order
  5. Append record to TP.wrdnm[] (append-only)
  6. Emit optional diagnostic audit record

No semantic interpretation, no free-form tokenization, no upstream mutation.

Aligned with:
  - 20.44_wrdnm_primitive.md
  - wrdnm_software_architecture.md
  - wrdnm_py_struc_pgm.md
  - progressive_lineup_testing.md v4.0
"""

import os
import copy
import yaml
from datetime import datetime, timezone

PRIMITIVE_NAME = "wrdnm"


def get_primitive_name():
    return PRIMITIVE_NAME


# ------------------------------------------------------------
# Pure-Python MurmurHash3 32-bit (deterministic, fixed seed)
# ------------------------------------------------------------
def _murmur3_32(data: bytes, seed: int = 0) -> int:
    """MurmurHash3 x86 32-bit. Returns unsigned 32-bit int."""
    c1 = 0xCC9E2D51
    c2 = 0x1B873593
    length = len(data)
    h1 = seed & 0xFFFFFFFF
    rounded_end = (length & ~0x3)

    for i in range(0, rounded_end, 4):
        k1 = (
            data[i]
            | (data[i + 1] << 8)
            | (data[i + 2] << 16)
            | (data[i + 3] << 24)
        )
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xE6546B64) & 0xFFFFFFFF

    k1 = 0
    tail_index = rounded_end
    tail_size = length & 0x3
    if tail_size >= 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    h1 ^= length
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85EBCA6B) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xC2B2AE35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)
    return h1 & 0xFFFFFFFF


class WrdNm:
    def __init__(self, tp_input):
        self.tp = copy.deepcopy(tp_input) if tp_input else {}
        self._dir = os.path.dirname(__file__)
        self.schema = {}
        self.dicts = {}
        self.scalars = {}
        self.hash_cfg = {}
        self._conversion_decisions = []
        self._missing_fields = []
        self._dict_load_status = "ok"
        self._scalar_load_status = "ok"
        self._hash_config_status = "ok"

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def process(self):
        self._load_schema()
        self._load_resources()
        numeric = self._convert_fields()
        record = self._assemble_record(numeric)
        audit = self._build_audit_record()

        if "wrdnm" not in self.tp or not isinstance(self.tp.get("wrdnm"), list):
            self.tp["wrdnm"] = []
        self.tp["wrdnm"].append(record)

        if "metadata" not in self.tp or not isinstance(self.tp.get("metadata"), dict):
            self.tp["metadata"] = {}
        self.tp["metadata"]["wrdnm_audit_record"] = audit

        return self.tp

    # ----------------------------------------------------------
    # Loading
    # ----------------------------------------------------------

    def _load_schema(self):
        path = os.path.join(self._dir, "wrdnm_schema.yaml")
        if not os.path.exists(path):
            self.schema = {"fields": {}, "canonical_order": []}
            return
        with open(path, "r", encoding="utf-8") as f:
            self.schema = yaml.safe_load(f) or {}

    def _load_resources(self):
        fields = self.schema.get("fields") or {}
        dict_files = set()
        scalar_files = set()

        for meta in fields.values():
            if not isinstance(meta, dict):
                continue
            if meta.get("dictionary"):
                dict_files.add(meta["dictionary"])
            if meta.get("scalar_table"):
                scalar_files.add(meta["scalar_table"])
            if meta.get("hash_config"):
                # load hash config once
                hc_name = meta["hash_config"]
                hc_path = os.path.join(self._dir, hc_name)
                if os.path.exists(hc_path):
                    with open(hc_path, "r", encoding="utf-8") as f:
                        self.hash_cfg = yaml.safe_load(f) or {}
                    self._hash_config_status = "ok"
                else:
                    self.hash_cfg = {
                        "hash_algorithm": "murmur3_32",
                        "seed": 4278190080,
                        "fallback": 0,
                    }
                    self._hash_config_status = "fail"

        loaded_dicts = 0
        for name in dict_files:
            path = os.path.join(self._dir, name)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    raw = yaml.safe_load(f) or {}
                # strip comment-only / non-mapping noise; keep str→number
                clean = {}
                if isinstance(raw, dict):
                    for k, v in raw.items():
                        if isinstance(k, str) and not k.startswith("#"):
                            try:
                                clean[str(k).lower()] = float(v)
                            except (TypeError, ValueError):
                                continue
                self.dicts[name] = clean
                loaded_dicts += 1
            else:
                self.dicts[name] = {}

        if dict_files and loaded_dicts == 0:
            self._dict_load_status = "fail"
        elif dict_files and loaded_dicts < len(dict_files):
            self._dict_load_status = "partial"
        else:
            self._dict_load_status = "ok"

        loaded_scalars = 0
        for name in scalar_files:
            path = os.path.join(self._dir, name)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    raw = yaml.safe_load(f) or {}
                clean = {}
                if isinstance(raw, dict):
                    for k, v in raw.items():
                        if isinstance(k, str) and not k.startswith("#"):
                            try:
                                clean[str(k).lower()] = float(v)
                            except (TypeError, ValueError):
                                continue
                self.scalars[name] = clean
                loaded_scalars += 1
            else:
                self.scalars[name] = {}

        if scalar_files and loaded_scalars == 0:
            self._scalar_load_status = "fail"
        elif scalar_files and loaded_scalars < len(scalar_files):
            self._scalar_load_status = "partial"
        else:
            self._scalar_load_status = "ok"

        # Ensure hash config even if no hashed field declared
        if not self.hash_cfg:
            hc_path = os.path.join(self._dir, "hash_config.yaml")
            if os.path.exists(hc_path):
                with open(hc_path, "r", encoding="utf-8") as f:
                    self.hash_cfg = yaml.safe_load(f) or {}
                self._hash_config_status = "ok"
            else:
                self.hash_cfg = {
                    "hash_algorithm": "murmur3_32",
                    "seed": 4278190080,
                    "fallback": 0,
                }
                self._hash_config_status = "fail"

    # ----------------------------------------------------------
    # Nested field access
    # ----------------------------------------------------------

    def _resolve_path(self, path_str):
        """Resolve dotted path against self.tp. Returns (found, value)."""
        if not path_str or not isinstance(path_str, str):
            return False, None
        parts = path_str.split(".")
        cur = self.tp
        for p in parts:
            if not isinstance(cur, dict) or p not in cur:
                return False, None
            cur = cur[p]
        return True, cur

    # ----------------------------------------------------------
    # Conversion
    # ----------------------------------------------------------

    def _convert_fields(self):
        fields = self.schema.get("fields") or {}
        order = self.schema.get("canonical_order") or list(fields.keys())
        result = {}

        for out_key in order:
            meta = fields.get(out_key)
            if not isinstance(meta, dict):
                continue

            tp_path = meta.get("tp_field")
            mtype = meta.get("mapping_type", "categorical")
            found, value = self._resolve_path(tp_path)

            if not found or value is None or value == "":
                self._missing_fields.append(tp_path or out_key)
                # defaults by type
                if mtype == "boolean":
                    result[out_key] = 0
                elif mtype == "hashed":
                    result[out_key] = int(self.hash_cfg.get("fallback", 0))
                elif mtype == "scalar":
                    result[out_key] = 0.0
                else:
                    result[out_key] = 0.0
                self._conversion_decisions.append(
                    f"{out_key}: missing → fallback"
                )
                continue

            if mtype == "categorical":
                dict_name = meta.get("dictionary")
                table = self.dicts.get(dict_name, {})
                key = str(value).lower().strip()
                if key in table:
                    result[out_key] = float(table[key])
                    self._conversion_decisions.append(
                        f"{out_key}: {key} → {result[out_key]}"
                    )
                else:
                    result[out_key] = 0.0
                    self._conversion_decisions.append(
                        f"{out_key}: {key} missing in dict → 0.0"
                    )

            elif mtype == "boolean":
                if isinstance(value, bool):
                    result[out_key] = 1 if value else 0
                elif isinstance(value, (int, float)):
                    result[out_key] = 1 if value else 0
                else:
                    s = str(value).lower().strip()
                    result[out_key] = 1 if s in ("true", "1", "yes", "y") else 0
                self._conversion_decisions.append(
                    f"{out_key}: boolean → {result[out_key]}"
                )

            elif mtype == "scalar":
                table_name = meta.get("scalar_table")
                table = self.scalars.get(table_name, {})
                key = str(value).lower().strip()
                if key in table:
                    result[out_key] = float(table[key])
                    self._conversion_decisions.append(
                        f"{out_key}: {key} → {result[out_key]}"
                    )
                else:
                    # allow already-numeric values
                    try:
                        result[out_key] = float(value)
                        self._conversion_decisions.append(
                            f"{out_key}: numeric passthrough → {result[out_key]}"
                        )
                    except (TypeError, ValueError):
                        result[out_key] = 0.0
                        self._conversion_decisions.append(
                            f"{out_key}: {key} missing in scalar → 0.0"
                        )

            elif mtype == "hashed":
                seed = int(self.hash_cfg.get("seed", 4278190080))
                s = str(value)
                if not s:
                    result[out_key] = int(self.hash_cfg.get("fallback", 0))
                    self._conversion_decisions.append(
                        f"{out_key}: empty hash → fallback"
                    )
                else:
                    h = _murmur3_32(s.encode("utf-8"), seed)
                    result[out_key] = int(h)
                    self._conversion_decisions.append(
                        f"{out_key}: hash → {result[out_key]}"
                    )

            else:
                result[out_key] = 0.0
                self._conversion_decisions.append(
                    f"{out_key}: unknown mapping_type {mtype} → 0.0"
                )

        return result

    # ----------------------------------------------------------
    # Record assembly
    # ----------------------------------------------------------

    def _assemble_record(self, numeric):
        order = self.schema.get("canonical_order") or list(numeric.keys())
        record = {}
        for key in order:
            if key in numeric:
                record[key] = numeric[key]
        # ensure any converted keys not in order still appear
        for key, val in numeric.items():
            if key not in record:
                record[key] = val

        record["provenance"] = {
            "origin": "WrdNm",
            "last_update": "WrdNm",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return record

    def _build_audit_record(self):
        return {
            "dictionary_load_status": self._dict_load_status,
            "scalar_table_load_status": self._scalar_load_status,
            "hash_config_status": self._hash_config_status,
            "conversion_decisions": list(self._conversion_decisions),
            "missing_fields": list(self._missing_fields),
            "provenance_lineage": {
                "origin": "WrdNm",
                "last_update": "WrdNm",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
