# Claim backlog rest — one merge, not finished

The table is not one merge away from done.

Already wired on main: negation, coordination, conditional, fragment, speaker, passive, quantifier, and the action op. Command and request have an `imperative` card. The runner pass before that card did not print their lines, because `modifier_resolution` still writes `selected_ops` from the builder, and the builder did not yet extend the force ops.

This branch adds the exclamative card, filed residual because the family enum has no exclamative family. It does not yet bind that card in `registry.py`, and it does not yet extend `_build_selected_ops`. Those two edits were not included after earlier partial writes truncated modules.

So this is not the completing merge. The remaining packet lines are `bare_command`, `polite_request`, and `exclamative_force`, and they need the builder extend plus the registry bind before a runner replay can show them.
