# Connection

**Date:** 2026-10-08
**Status:** the mapping unit for this pass. Not a new IdOB family.

Front door: [README.md](README.md).

One connection is two objects taken from the packet, one relation taken from a hat or an op, and one status.

```text
left, relation, right, status
```

`status` is `supported` or `missing`. There is no likelihood field and no history field.

`supported` requires both ends to be non-empty packet fields and the relation to be on the closed list for this pass:

`speaker`, `reporting`, `theme`, `state`, `location`, `copula`, `action`, `patient`, `recipient`, `relative_subject`, `query_focus`, `adverb`.

A relation not on that list is a pressure point. It is not added inside a composition.

A composition is the utterance, the supported connections, and the holes. The readable claim in [../s2m_rung1.md](../s2m_rung1.md) is a separate projection. If the claim and the connections disagree, the disagreement is reported. It is not repaired here.
