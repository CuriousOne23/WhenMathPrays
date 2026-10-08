# Action row — verb circle landed on this branch

**Replay:** `PYTHONPATH=. python3 support/tools/action_row_replay.py`

*The cat chased the mouse.* segments `NP VP NP`, cue `action_clause`, op `agent_action`. `modifier_resolution` still prints beside a non-empty cue list. That is the old helper, not the action claim.

*The sky is blue.* prints no op.
*Close the door.* still prints `bare_command`.

The form is token classes for `chased`, `chase`, `chases`, `bought`, `buy`, `wrote`, `write`, plus `cat` and `mouse`. SOB already had a `VP` pattern. CnOB and SmOB already wrote `action_clause_rule` and `action_clause` when a `VP` and one of those verbs are present. This pass did not edit `primitives_pathA_short.py`.

The three form holes remain named. They are not this pass.


## Earlier branch fact

# Action row — runner result, code not on this branch

**Branch fact (still).** Comprehensive status: [program/ready_line.md](program/ready_line.md). Coverage claims that this row already prints on `main` are superseded by this page.


Local runner after a form split:

*The cat chased the mouse.* segments `NP VP NP`, cue `action_clause`, op `agent_action`.  
*The sky is blue.* still prints no op.  
*Close the door.* still prints `bare_command`.

The edit is a verb circle for `chased`, `chase`, `chases`, `bought`, `buy`, `wrote`, `write`, plus an `action_clause` cue, plus `agent_action` on the builder. It is not uploaded here. A partial write of `primitives_pathA_short.py` has truncated modules before, so this branch does not pretend the file landed.

The claim backlog table prints on that local runner. It is not complete on `main` until this form edit is applied and replayed there.
