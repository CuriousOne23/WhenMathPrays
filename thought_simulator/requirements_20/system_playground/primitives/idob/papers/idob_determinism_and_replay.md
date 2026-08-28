# IdOB determinism and replay (S2M)

Same frozen YAML revision + same (`utterance` or `card_id`) + same `packs_loaded` + same `cie_id` + same `prior_M` → same `tp.idob` packet (including Δh and flags).

Utterance must be stored on the packet even on miss so a trace can be replayed without guessing the carrier.

Not deterministic across **dictionary edits**. That is a new revision. Record the file set in the TP provenance when you care.

Lifecycle replay of formation…closure envelopes is a different fixture set (`lifecycle/`).
