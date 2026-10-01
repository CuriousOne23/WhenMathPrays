# Bench walk 8 — the stamped card

**Look at:** the passport page after the stamps.  
**Token:** `idob_packet`. Step 10. Meaning on this path.  
**Authority:** [IdOB_unified_plan.md](../../architecture/IdOB_unified_plan.md), [idob_meaning_lock.md](../../architecture/idob_meaning_lock.md)  
**Next:** [09_empty_hook.md](09_empty_hook.md)

False image: the meaning was retrieved from a shelf.  
On the bench: the card after every stamp that was allowed to fire has pressed.  
Nearest picture: the passport page after the stamps, not the country.

Identity Observation Block (IdOB) is the sum, not an object:

\[
\mathrm{IdOB}(U)=\bigoplus_{o\in A(U)} c_o
\]

The \(o\) are stamp cards. The right-hand side is this page. Output Binding / Assemble (OuBA) locks the page in the folder. It does not add a stamp and it does not finalize a second meaning.

Honest cards, teaching only:

- *The sky is blue.* Declarative. Copular stamp. Lines `theme` and `state`. Overlap need not fire.
- *The book is on the table.* Declarative locative. Lines `theme` and `location`.
- *Where is the book that is on the table?* Interrogative mood. More than one stamp. Overlap may be nonempty.

`identity_geometry` is a field on this card: `structural_identity`, `referential_identity`, or `semantic_identity`. An indicator of what fired, plus claimed roles. It is not the Cognitive Identity Envelope (CIE).

`meaning_delta` on this card is a writer-diff. It is not \(\Delta h\).

Accomplishment is `complete` on the packet. It does not rename a stamp into the card.
