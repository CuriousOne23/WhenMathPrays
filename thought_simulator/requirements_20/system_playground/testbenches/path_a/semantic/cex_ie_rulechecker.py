# cex_ie_rulechecker.py
# Rule-driven validator for CEx-IE in general mode
# Uses cex_ie_rules.yaml to check TP.cex.ie output against primitive rules.

import yaml


class CExIERuleChecker:
    def __init__(self, rules_path: str):
        with open(rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.ruleset = data.get("ruleset", {})

    # -----------------------------
    # Public API
    # -----------------------------
    def check(self, tp_input: dict, tp_output: dict) -> dict:
        """
        tp_input: full TP envelope before CEx-IE
        tp_output: full TP envelope after CEx-IE (including TP.cex.ie)
        Returns: dict with { "pass": bool, "errors": [str] }
        """
        errors = []

        cex_ie = self._get_cex_ie(tp_output, errors)
        if cex_ie is None:
            return {"pass": False, "errors": errors}

        self._check_envelope_shape(cex_ie, errors)
        self._check_deterministic_copy(tp_input, cex_ie, errors)
        self._check_structural_phrases(cex_ie, errors)
        self._check_hints(cex_ie, tp_input, errors)
        self._check_bounded_semantics(errors)
        self._check_determinism(errors)
        self._check_boundaries(tp_input, tp_output, errors)
        self._check_consistency(cex_ie, errors)
        self._apply_error_rules(errors)

        return {"pass": len(errors) == 0, "errors": errors}

    # -----------------------------
    # Helpers
    # -----------------------------
    def _get_cex_ie(self, tp_output, errors):
        try:
            return tp_output["TP"]["cex"]["ie"]
        except Exception:
            errors.append("Missing TP.cex.ie envelope in output.")
            return None

    def _check_envelope_shape(self, cex_ie, errors):
        env_rules = self.ruleset.get("envelope", {})
        required = env_rules.get("required_fields", [])
        forbidden = env_rules.get("forbidden_fields", [])
        field_types = env_rules.get("field_types", {})

        for field in required:
            if field not in cex_ie:
                errors.append(f"Missing required field: {field}")

        for field in forbidden:
            if field in cex_ie:
                errors.append(f"Forbidden field present in TP.cex.ie: {field}")

        for field, ftype in field_types.items():
            if field not in cex_ie:
                continue
            value = cex_ie[field]
            if ftype == "list" and not isinstance(value, list):
                errors.append(f"Field {field} must be a list.")
            if ftype == "string" and not isinstance(value, str):
                errors.append(f"Field {field} must be a string.")

    def _check_deterministic_copy(self, tp_input, cex_ie, errors):
        rules = self.ruleset.get("deterministic_copy", {})
        intake = tp_input.get("TP", {}).get("intake", {})

        if rules.get("tokens_must_match_ie", False):
            src = intake.get("ie_tokens", [])
            dst = cex_ie.get("tokens", [])
            if src != dst:
                errors.append("tokens do not match TP.intake.ie_tokens.")

        if rules.get("token_flags_must_match_ie", False):
            src = intake.get("token_flags", [])
            dst = cex_ie.get("token_flags", [])
            if src != dst:
                errors.append("token_flags do not match TP.intake.token_flags.")

        if rules.get("normalized_text_must_match_ie", False):
            src = intake.get("normalized_text", "")
            dst = cex_ie.get("normalized_text", "")
            if src != dst:
                errors.append("normalized_text does not match TP.intake.normalized_text.")

    def _check_structural_phrases(self, cex_ie, errors):
        rules = self.ruleset.get("structural_phrases", {})
        allowed_prefixes = rules.get("allowed_prefixes", [])
        max_phrases = rules.get("max_phrases", 10)

        phrases = cex_ie.get("structural_phrases", [])
        if len(phrases) > max_phrases:
            errors.append(f"Too many structural_phrases: {len(phrases)} > {max_phrases}.")

        if rules.get("require_prefix", True):
            for p in phrases:
                if not any(p.startswith(pref) for pref in allowed_prefixes):
                    errors.append(f"Structural phrase has invalid prefix: {p}")

    def _check_hints(self, cex_ie, tp_input, errors):
        hint_rules = self.ruleset.get("hints", {})
        intake = tp_input.get("TP", {}).get("intake", {})
        structure = tp_input.get("TP", {}).get("structure", {})
        metadata = tp_input.get("TP", {}).get("metadata", {})

        for hint_name, cfg in hint_rules.items():
            allowed = cfg.get("allowed", [])
            value = cex_ie.get(hint_name)
            if value not in allowed:
                errors.append(f"{hint_name} has invalid value: {value}, allowed: {allowed}")

        # coherence_hint special check
        coherence_cfg = hint_rules.get("coherence_hint", {})
        coherence_val = cex_ie.get("coherence_hint")
        if coherence_val == "stable":
            # if anomaly spans or repair_annotations exist, stable may be suspicious
            spans = structure.get("spans", [])
            repairs = metadata.get("repair_annotations", [])
            anomaly_spans = [s for s in spans if "anomaly" in s.get("type", "")]
            if anomaly_spans or repairs:
                errors.append("coherence_hint=stable but anomaly/repair metadata present.")

    def _check_bounded_semantics(self, errors):
        rules = self.ruleset.get("bounded_semantics", {})
        # These are mostly configuration flags; we just assert they are set correctly.
        if not rules.get("no_embeddings", True):
            errors.append("Bounded semantics violation: embeddings allowed.")
        if not rules.get("no_global_semantics", True):
            errors.append("Bounded semantics violation: global semantics allowed.")
        if not rules.get("no_contextual_semantics", True):
            errors.append("Bounded semantics violation: contextual semantics allowed.")
        if not rules.get("no_cross_sentence_semantics", True):
            errors.append("Bounded semantics violation: cross-sentence semantics allowed.")

    def _check_determinism(self, errors):
        # Determinism is enforced at the framework level (replay tests).
        # Here we just ensure flags are set as expected.
        rules = self.ruleset.get("determinism", {})
        if not rules.get("identical_input_produces_identical_output", True):
            errors.append("Determinism rule misconfigured: identical_input_produces_identical_output must be true.")

    def _check_boundaries(self, tp_input, tp_output, errors):
        rules = self.ruleset.get("boundaries", {})
        forbidden_writes = rules.get("forbidden_writes", [])

        # We assume tp_output is the full TP; we just check that only TP.cex.ie changed.
        # In practice, the testbench compares pre/post envelopes; here we enforce config.
        for field in forbidden_writes:
            parts = field.split(".")
            cur = tp_output
            for p in parts:
                if p in cur:
                    errors.append(f"Forbidden write detected in field: {field}")
                    break
                if isinstance(cur, dict):
                    cur = cur.get(p, {})
                else:
                    break

    def _check_consistency(self, cex_ie, errors):
        rules = self.ruleset.get("consistency", {})

        topic = cex_ie.get("topic_hint")
        intent = cex_ie.get("intent_hint")
        continuity = cex_ie.get("continuity_hint")
        reference = cex_ie.get("reference_hint")
        direction = cex_ie.get("direction_hint")
        politeness = cex_ie.get("politeness_hint")
        register = cex_ie.get("register_hint")

        if rules.get("topic_hint_consistent_with_intent", True):
            if topic == "greeting" and intent not in ("begin", "none"):
                errors.append("topic_hint=greeting inconsistent with intent_hint.")
            if topic == "assistance" and intent not in ("request", "inform"):
                errors.append("topic_hint=assistance inconsistent with intent_hint.")

        if rules.get("continuity_hint_consistent_with_reference", True):
            if continuity == "reset" and reference not in ("none",):
                errors.append("continuity_hint=reset inconsistent with reference_hint.")

        if rules.get("direction_hint_consistent_with_reference", True):
            if direction == "backward" and reference == "none":
                errors.append("direction_hint=backward but reference_hint=none.")

        if rules.get("politeness_hint_consistent_with_register", True):
            if politeness == "high" and register == "casual":
                errors.append("politeness_hint=high inconsistent with register_hint=casual.")

    def _apply_error_rules(self, errors):
        err_rules = self.ruleset.get("errors", {})
        # The framework will treat any collected errors as failure.
        # Here we just respect configuration flags; if misconfigured, we add an error.
        required_flags = [
            "fail_on_missing_required_field",
            "fail_on_forbidden_field_present",
            "fail_on_invalid_enum",
            "fail_on_invalid_phrase_prefix",
            "fail_on_non_deterministic_output",
        ]
        for flag in required_flags:
            if not err_rules.get(flag, True):
                errors.append(f"Error rule misconfigured: {flag} must be true.")


# Convenience function for testbench
def run_cex_ie_rulecheck(rules_path: str, tp_input: dict, tp_output: dict) -> dict:
    checker = CExIERuleChecker(rules_path)
    return checker.check(tp_input, tp_output)

