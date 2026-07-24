"""USP rule store prototype — read-only snapshot export; writes via UPI commit only."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_STRUCTS_PROTO = Path(__file__).resolve().parent.parent / "40.100_core_data_structs_prototypes" / "prototype.py"
_spec = importlib.util.spec_from_file_location("structs_prototype", _STRUCTS_PROTO)
_structs = importlib.util.module_from_spec(_spec)
sys.modules["structs_prototype"] = _structs
assert _spec.loader is not None
_spec.loader.exec_module(_structs)

UspRule = _structs.UspRule
UspSnapshot = _structs.UspSnapshot
UspVersionRecord = _structs.UspVersionRecord

DEFAULT_MAX_ACTIVE_RULES = 256

REASON_CAP_EXCEEDED = "USP_RSN_001_CAP_EXCEEDED"
REASON_GB_VETOED = "USP_RSN_002_GB_VETOED"
REASON_INVALID_TRANSITION = "USP_RSN_003_INVALID_TRANSITION"


class USPReject(ValueError):
    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


@dataclass
class CommitResult:
    ok: bool
    usp_version_id: int | None = None
    usp_version_ref: str | None = None
    active_rule_count: int = 0
    reason_codes: list[str] = field(default_factory=list)
    version_record: UspVersionRecord | None = None


class USPStore:
    """Versioned shorthand rule store with monotonic version_id."""

    def __init__(self, max_active_rules: int = DEFAULT_MAX_ACTIVE_RULES) -> None:
        self.max_active_rules = max_active_rules
        self._rules: list[UspRule] = []
        self._version_id = 0
        self._prior_ref: str | None = None
        self.version_records: list[UspVersionRecord] = []

    @property
    def version_id(self) -> int:
        return self._version_id

    def _active_rules(self) -> list[UspRule]:
        """ACTIVE rules sorted for store introspection.

        ``precedence`` affects IIInB apply ordering (20.102-012) but is excluded
        from ``usp_version_ref`` digest (40.100 ``compute_usp_version_ref``).
        """
        active = [r for r in self._rules if r.state == "ACTIVE"]
        return sorted(active, key=lambda r: (-r.precedence, -r.version, r.rule_id))

    def _snapshot(self) -> UspSnapshot:
        return UspSnapshot(usp_version_id=self._version_id, rules=list(self._rules))

    def export_snapshot(self) -> dict[str, Any]:
        """Read-only ACTIVE-only snapshot for IIInB (immutable handoff view)."""
        return self._snapshot().to_dict()

    def apply_commit(
        self,
        *,
        pattern: str,
        expansion: str,
        rule_id: str,
        transition: str = "create",
        gb_approved: bool = True,
        scope: str = "conversation",
    ) -> CommitResult:
        if not gb_approved:
            self.version_records.append(
                UspVersionRecord(
                    usp_version_id=self._version_id,
                    usp_version_ref=self._prior_ref or "",
                    prior_version_ref=self._prior_ref,
                    transition="gb_veto",
                )
            )
            return CommitResult(ok=False, reason_codes=[REASON_GB_VETOED])

        if transition == "create":
            if len(self._active_rules()) >= self.max_active_rules:
                return CommitResult(ok=False, reason_codes=[REASON_CAP_EXCEEDED])
            self._rules.append(
                UspRule(
                    rule_id=rule_id,
                    pattern=pattern,
                    expansion=expansion,
                    state="ACTIVE",
                    scope=scope,
                    version=1,
                )
            )
        elif transition == "supersede":
            target = next((r for r in self._rules if r.rule_id == rule_id and r.state == "ACTIVE"), None)
            if target is None:
                return CommitResult(ok=False, reason_codes=[REASON_INVALID_TRANSITION])
            target.state = "SUPERSEDED"
            self._rules.append(
                UspRule(
                    rule_id=rule_id,
                    pattern=pattern,
                    expansion=expansion,
                    state="ACTIVE",
                    scope=scope,
                    version=target.version + 1,
                )
            )
        elif transition == "revoke":
            target = next((r for r in self._rules if r.rule_id == rule_id and r.state == "ACTIVE"), None)
            if target is None:
                return CommitResult(ok=False, reason_codes=[REASON_INVALID_TRANSITION])
            target.state = "REVOKED"
        else:
            return CommitResult(ok=False, reason_codes=[REASON_INVALID_TRANSITION])

        prior = self._prior_ref
        self._version_id += 1
        snap = self._snapshot()
        ref = snap.version_ref
        record = UspVersionRecord(
            usp_version_id=self._version_id,
            usp_version_ref=ref,
            prior_version_ref=prior,
            transition=transition,
        )
        self.version_records.append(record)
        self._prior_ref = ref
        return CommitResult(
            ok=True,
            usp_version_id=self._version_id,
            usp_version_ref=ref,
            active_rule_count=len(self._active_rules()),
            version_record=record,
        )