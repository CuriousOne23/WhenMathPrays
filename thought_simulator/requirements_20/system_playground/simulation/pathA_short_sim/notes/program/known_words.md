# Known-word boundary

**Date:** 2026-10-08
**Status:** closed list. A word not on the list is not added by a claim.

The short sim does not repair an unknown content word into a known noun, adjective, or verb. A sentence outside the list misses until a word is added on purpose.

Replay: `PYTHONPATH=. python3 support/tools/known_word_boundary_replay.py`

- `zyzzyx qwop` has no circles and an empty claim.
- *The zyzzyx is blue.* does not claim a theme for `zyzzyx`.
- *The sky is zyzzyx.* does not claim `zyzzyx` as a state.
- *The sky is blue.* still claims `the sky is blue`.

This is not an invitation to grow the list in the claim rung. Add a word in the structure desks, then replay.

Program: [pathA_program.md](pathA_program.md). Claims: [claim_ledger.md](claim_ledger.md).
