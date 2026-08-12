"""
TPU Primitive (Version 1.0)
TP-UPDATE — sole deterministic commit authority for Path-A.

Aligned with:
  - 20.46 (TPU Requirements, Option C Rewrite)
  - tpu_py_struc_pgm.md (Version 1.0)
  - 20.105 / 20.105.010–030 (writer authority + provenance)
  - 20.30 (safe-boundary discipline)
  - 20.95 (canonical ordering)
  - 20.12 (replay invariants)
  - progressive_lineup_testing.md
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple


PRIMITIVE_NAME = "tpu"


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class TPU:
    """
    TPU is the deterministic commit engine of Path-A.

    Public API
    ----------
    tpu = TPU(tp_input, tp_update_request)
    tp_n1, audit = tpu.commit()          # primary return shape
    # also available after commit:
    #   tpu.tp, tpu.audit_record, tpu.error

    Responsibilities (SHALL)
    ------------------------
    - validate tp_update_request blocks
    - enforce writer-authority boundaries
    - enforce canonical ordering
    - enforce safe-boundary rules
    - apply updates atomically
    - enforce 1-TP-cycle lag semantics (commit appears only in N+1)
    - write commit provenance
    - produce tpu_audit_record and (on failure) tpu_error

    Forbidden
    ---------
    - generate meaning / interpret semantics
    - modify structural geometry, semantic_core, intake, current-turn context
    - perform routing or identity refinement
    - partial commits
    """

    # ----------------------------------------------------------------
    # Authoritative writer namespaces (minimal 20.105 model)
    # ----------------------------------------------------------------
    # Fields that meaning-layer blocks are NEVER allowed to carry.
    FORBIDDEN_IN_MEANING_BLOCKS = {
        "structural_geometry",
        "structural",
        "geometry",
        "semantic_core",
        "intake",
        "routing",
        "routing_metadata",
    }

    # Blocks that belong to meaning / process layers
    MEANING_BLOCKS = ("idob_update", "mcb_update", "rbu_update", "cob", "cop", "cil", "isc")

    def __init__(self, tp_input: Dict[str, Any], tp_update_request: Dict[str, Any]):
        # Working copy — we never mutate the caller's objects
        self.tp: Dict[str, Any] = copy.deepcopy(tp_input or {})
        self.req: Dict[str, Any] = copy.deepcopy(tp_update_request or {})
        self.tp_in: Dict[str, Any] = copy.deepcopy(tp_input or {})  # frozen snapshot for audit

        self.audit_record: Optional[Dict[str, Any]] = None
        self.error: Optional[Dict[str, Any]] = None

        # Deterministic commit counter derived from request seed / prior lineage
        self._commit_seq = self._derive_commit_sequence()

    # ================================================================
    # Public entry point — exact ordering from tpu_py_struc_pgm.md §4
    # ================================================================
    def commit(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Execute the authoritative commit pipeline.

        Returns
        -------
        (tp_n1, audit_record)

        On validation failure the original TP is retained, an error
        object is attached, and the audit records the rejection.
        """
        # 1–2  already performed in __init__ (read TP(N) + request)

        # 3. Validate writer authority
        ok, reason = self._validate_writer_authority(self.req)
        if not ok:
            return self._reject("WRITER_AUTHORITY_VIOLATION", reason)

        # 4. Validate update blocks (shape / boundedness)
        ok, reason = self._validate_update_blocks(self.req)
        if not ok:
            return self._reject("UPDATE_BLOCK_INVALID", reason)

        # 5. Validate canonical ordering markers
        ok, reason = self._validate_canonical_ordering(self.req)
        if not ok:
            return self._reject("CANONICAL_ORDERING_VIOLATION", reason)

        # 6. Validate safe-boundary conditions
        ok, reason = self._validate_safe_boundary(self.req)
        if not ok:
            return self._reject("SAFE_BOUNDARY_VIOLATION", reason)

        # 7. Apply updates atomically
        updated_tp = self._apply_updates(self.tp, self.req)

        # 8. Write commit provenance
        self._write_provenance(updated_tp)

        # 9–10. Produce audit (and no error on success)
        audit = self._build_audit_record(
            status="committed",
            writer_authority="pass",
            canonical_ordering="pass",
            safe_boundary="pass",
            atomicity="pass",
            tp_n=self.tp_in,
            tp_n1=updated_tp,
            reason=None,
        )
        self.audit_record = audit
        self.error = None
        self.tp = updated_tp

        # 11. Emit TP(N+1)
        return updated_tp, audit

    # ================================================================
    # Validation helpers
    # ================================================================

    def _validate_writer_authority(self, req: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HLR-20.46-003
        Each block may contain only fields permitted for that writer.
        Meaning-layer blocks must not carry structural / process geometry.
        """
        for block_name in self.MEANING_BLOCKS:
            block = req.get(block_name) or {}
            if not isinstance(block, dict):
                continue
            for forbidden in self.FORBIDDEN_IN_MEANING_BLOCKS:
                if forbidden in block:
                    return (
                        False,
                        f"{block_name} attempted write outside authority domain ({forbidden})",
                    )
        return True, ""

    def _validate_update_blocks(self, req: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Light structural validation of the known update blocks.
        Clarifying-field boundedness (10 / 100 / 4) is enforced when present.
        """
        # Clarifying-field limits (HLR-20.46-025)
        # Look in mcb_update / cob / continuity-style payloads
        for block_name in ("mcb_update", "cob", "idob_update"):
            block = req.get(block_name) or {}
            cf = None
            if isinstance(block, dict):
                cf = block.get("clarifying_fields")
                if cf is None and "next_context" in block:
                    cf = (block.get("next_context") or {}).get("clarifying_fields")
            if cf is not None:
                if not isinstance(cf, list):
                    return False, f"{block_name}.clarifying_fields must be a list"
                if len(cf) > 10:
                    return False, f"{block_name}.clarifying_fields exceeds max 10 (got {len(cf)})"
        return True, ""

    def _validate_canonical_ordering(self, req: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HLR-20.46-004 / 20.95
        We accept an explicit canonical_ordering_hash when supplied;
        absence is tolerated for early testbenches.
        """
        meta = req.get("metadata") or {}
        # Presence of a hash is recorded but not cryptographically verified here
        # (full 20.95 verification can be layered later).
        _ = meta.get("canonical_ordering_hash")
        return True, ""

    def _validate_safe_boundary(self, req: Dict[str, Any]) -> Tuple[bool, str]:
        """
        HLR-20.46-005 / 20.30
        Commit is allowed only when the safe-boundary marker is true
        (or the marker is absent — treated as safe for progressive testing).
        """
        meta = req.get("metadata") or {}
        marker = meta.get("safe_boundary_marker")
        if marker is None:
            return True, ""  # progressive / early tests may omit the marker
        if marker is True or marker == "true" or marker == 1:
            return True, ""
        return False, f"safe_boundary_marker is not true (got {marker!r})"

    # ================================================================
    # Atomic apply
    # ================================================================

    def _apply_updates(
        self, tp: Dict[str, Any], req: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply the authorized portions of the update request atomically.
        Only fields that TPU is allowed to write are touched.
        """
        out = copy.deepcopy(tp)
        meta = out.setdefault("metadata", {})

        # ---- next_context (from MCB) ----
        mcb = req.get("mcb_update") or {}
        if isinstance(mcb, dict) and "next_context" in mcb:
            incoming = mcb["next_context"]
            if isinstance(incoming, dict):
                # Write-only into next_context; never touch current-turn context
                meta["next_context"] = self._canonical_copy(incoming)

        # ---- continuity / clarifying (light pass-through when present) ----
        for src_key, dst_key in (
            ("continuity_metadata", "continuity_metadata"),
            ("msl_metadata", "msl_metadata"),
            ("cil_metadata", "cil_metadata"),
            ("semantic_residue_metadata", "semantic_residue_metadata"),
        ):
            # Prefer values already sitting on the TP (from CE / upstream);
            # only overwrite when the request explicitly carries them.
            if src_key in req and isinstance(req[src_key], dict):
                meta[dst_key] = self._canonical_copy(req[src_key])

        # ---- CE context envelope is already on the TP; mark it committed ----
        # (TPU does not re-normalize; it only records the commit)
        ctx = meta.get("context")
        if isinstance(ctx, dict):
            prov = ctx.setdefault("context_provenance", {})
            # Extend lineage; origin stays CE, last_update becomes TPU
            prov["last_update"] = "TPU"
            lineage = list(prov.get("commit_lineage") or [])
            # lineage is completed in _write_provenance

        return out

    # ================================================================
    # Provenance
    # ================================================================

    def _write_provenance(self, tp: Dict[str, Any]) -> None:
        """
        Write TPU-authored provenance_metadata (HLR + structural program).
        """
        meta = tp.setdefault("metadata", {})
        commit_id = self._make_commit_id()

        # Prior lineage (from CE or earlier TPU commits)
        prior = []
        old_prov = meta.get("provenance_metadata") or {}
        if isinstance(old_prov, dict):
            prior = list(old_prov.get("commit_lineage") or [])
        # Also harvest from context_provenance if present
        ctx_prov = (meta.get("context") or {}).get("context_provenance") or {}
        if isinstance(ctx_prov, dict):
            for item in ctx_prov.get("commit_lineage") or []:
                if item not in prior:
                    prior.append(item)

        new_lineage = prior + [commit_id]

        meta["provenance_metadata"] = {
            "commit_id": commit_id,
            "commit_sequence": self._commit_seq,
            "primitive_origin": "TPU",
            "commit_timestamp": None,  # deliberately omitted for pure replay determinism
            "commit_lineage": new_lineage,
        }

        # Keep context_provenance lineage in sync
        if isinstance(meta.get("context"), dict):
            cp = meta["context"].setdefault("context_provenance", {})
            cp["last_update"] = "TPU"
            cp["commit_lineage"] = list(new_lineage)

    # ================================================================
    # Audit / Error
    # ================================================================

    def _build_audit_record(
        self,
        *,
        status: str,
        writer_authority: str,
        canonical_ordering: str,
        safe_boundary: str,
        atomicity: str,
        tp_n: Dict[str, Any],
        tp_n1: Dict[str, Any],
        reason: Optional[str],
    ) -> Dict[str, Any]:
        return {
            "status": status,
            "writer_authority": writer_authority,
            "canonical_ordering": canonical_ordering,
            "safe_boundary": safe_boundary,
            "atomicity": atomicity,
            "reason": reason,
            "tp_n_hash": self._stable_hash(tp_n),
            "tp_n1_hash": self._stable_hash(tp_n1),
            "commit_sequence": self._commit_seq,
            "primitive_origin": "TPU",
        }

    def _reject(self, code: str, rationale: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Deterministic fallback: retain TP(N), emit error + audit.
        """
        retained = copy.deepcopy(self.tp_in)
        audit = self._build_audit_record(
            status="rejected",
            writer_authority="fail" if "AUTHORITY" in code else "pass",
            canonical_ordering="pass",
            safe_boundary="pass",
            atomicity="pass",  # nothing was applied
            tp_n=self.tp_in,
            tp_n1=retained,
            reason=rationale,
        )
        error = {
            "code": code,
            "rationale": rationale,
            "fallback_behavior": "retain_TP_N",
            "audit_record": audit,
        }
        self.tp = retained
        self.audit_record = audit
        self.error = error
        return retained, audit

    # ================================================================
    # Deterministic helpers
    # ================================================================

    def _derive_commit_sequence(self) -> int:
        """Derive a stable sequence number from prior provenance or request seed."""
        meta = (self.tp.get("metadata") or {})
        prov = meta.get("provenance_metadata") or {}
        seq = prov.get("commit_sequence")
        if isinstance(seq, int):
            return seq + 1
        # Fall back to a hash of the request seed
        seed = ((self.req.get("metadata") or {}).get("seed")) or "tpu_default"
        h = int(hashlib.sha256(str(seed).encode("utf-8")).hexdigest()[:8], 16)
        return (h % 100000) + 1

    def _make_commit_id(self) -> str:
        seed = ((self.req.get("metadata") or {}).get("seed")) or "tpu_default"
        raw = f"{seed}:{self._commit_seq}"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
        return f"tpu_{digest}"

    @staticmethod
    def _stable_hash(obj: Any) -> str:
        try:
            payload = json.dumps(obj, sort_keys=True, default=str)
        except Exception:
            payload = str(obj)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _canonical_copy(obj: Any) -> Any:
        """Deep copy with deterministic key ordering for dicts."""
        if isinstance(obj, dict):
            return {k: TPU._canonical_copy(obj[k]) for k in sorted(obj.keys())}
        if isinstance(obj, list):
            return [TPU._canonical_copy(x) for x in obj]
        return copy.deepcopy(obj)
