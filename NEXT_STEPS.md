# Next Steps for WhenMathPrays

This checklist preserves clarity while guiding future stewardship.

## Documentation
- [*] Annotate lineage: ULep → UREP transition and rationale
- [*] Add principle templates (Markdown) with scope, implementation, testability
- [ ] Refine workflow for rendering equations (cartesian averaging, gamma_self)

## Simulations
- [ ] Synchronize and annotate canonical γ_self trajectory for M1
- [ ] Modularize simulation ethos into documentation
- [ ] Compose musical motifs for each movement (breath intervals as signals)

## Stewardship
- [ ] Codify UREP’s definition of relational intensity
- [ ] Document rationale for unbounded γ_self
- [ ] Maintain editorial clarity and modularity across all files

---

## Equation Rendering Workflow

To ensure clarity and fidelity in UREP documentation:

- **Format:** Write all equations in LaTeX inside Markdown (`\( ... \)` for inline, `

\[ ... \]

` or `$$ ... $$` for block).
- **Rendering:** Prefer MathJax for live rendering; if unavailable, export PNG snippets for embedding.
- **Orientation:** Document that γ_self is computed via cartesian averaging of 2D vectors to prevent wrap artifacts.
- **Dimensionality:** Preserve γ_self as 2D, making Love a 2D vector scaled by scalar gates.
- **Annotation:** Each equation should be modular and standalone, with rationale noted for mathematical choices.

