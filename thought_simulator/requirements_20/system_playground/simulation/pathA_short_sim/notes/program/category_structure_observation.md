# Category Structure Observation

**Document:** notes/program/category_structure_observation.md  
**Status:** Experimental / observational paper. Not a normative requirement. Not a replacement for s2m_relational_proposal.md, s2m_program_reference.md, or category_selection_proposal.md.  
**Date:** 2026-11-20  
**Phase:** IV — Category Structure Observation  
**Instrument:** run_examples.py (reading manual: user_guide.md)

## Purpose

This paper defines and records a bounded three-experiment Phase IV program.

Its central purpose is to use the characterized S2M realization as a controlled, inspectable, and replayable instrument for observing how information affects relational participation in realized meaning.

It preserves the methodological distinction:

conceptual definition → functional realization → realization characterization → category structure observation

Phase IV does not redesign the simulator while observing it. It uses the characterized realization as the experimental instrument.

Authorities (read, not modified here):
- [s2m_relational_proposal.md](s2m_relational_proposal.md) — conceptual authority for the five-stage S2M model (structural relation → default meaning → candidate interpretation space → selected interpretive extension(s) → finite customized composite).
- [s2m_program_reference.md](s2m_program_reference.md) — executable contract; Phase III Realization Characterization; Phase IV Category Structure Observation and its epistemic boundary.
- [category_selection_proposal.md](category_selection_proposal.md) — bounded category-selection phenomenon.
- [user_guide.md](../../user_guide.md) — instrument-reading manual for normal run_examples.py output.

## Experimental method

Common procedure for all Phase IV experiments:

define the question → identify base variables → identify the intentionally varied condition → hold the remaining conditions fixed where possible → run the existing observation instrument → record intermediate states → compare control and experimental conditions → replay under identical conditions → identify invariants and differences → state the bounded conclusion

The object of observation is not merely the final semantic output. The experiment may inspect the realized progression:

structural/default basis → information/cue state → category evidence → candidate availability/relevance → legitimation/refusal → participating/non-participating relation → final composite

Terminology follows the S2M documents.

## Experimental instrument

`run_examples.py` is the normal Phase IV observation instrument.  
`user_guide.md` is the instrument-reading manual.

The GitHub Agent may execute, capture, and compare runs, but the Agent is not the experimental instrument. Observable evidence must remain available through the simulator output itself. Field interpretation is referenced from the user guide rather than duplicated here.

## Observation versus interpretation

For each experiment, observations are separated into:
- **Observed**: what the instrument actually displayed.
- **Interpretation**: what can reasonably be said about the current TS realization from those observations.
- **Not established**: claims the experiment does not support.
- **Conjecture / future question**: questions motivated by the observations but not established by them.

**Epistemic boundary:** An observation characterizes behavior of the current realization. It does not independently establish a new requirement, semantic truth, or architectural claim.

---

## Experiment 1 — Context and relational participation

**Status:** Completed

**Experimental question**  
Can additional contextual information change whether already-available relational possibilities participate in realized meaning while the sentence, structural relation, and structurally derived default meaning remain unchanged?

**Controlled comparison**  
Control: sentence “The book is on the table.” with no prior-context category information. Conceptually: $S_{\text{same}} + C_{\varnothing}$.  
Experimental condition: same sentence with the existing prior-context observation condition. Conceptually: $S_{\text{same}} + C_{\text{prior}}$.

**Base variables held constant** (within the bounded realization)  
- sentence  
- structural relation  
- structurally derived default meaning  
- candidate interpretation inventory  
- simulator realization/configuration

**Intentionally changed condition**  
prior-context information.

The methodological question is: where does the additional information first enter, how is it propagated, and at what point does it become consequential to relational participation?

**Observed progression**  
Control: candidate relations available but unselected.  
Prior-context condition: additional information flowing through the contextual/category path, resulting in candidate relations becoming relevant and, after the bounded legitimation step, participating in the final composite.

Observational sequence (organization of the current realized experiment, not a universal theory):

relation available → additional information → relation becomes relevant → legitimation or refusal → relation participates or does not participate in realized meaning

**Results and conclusion**  
Within the current bounded TS realization, additional contextual information can change whether already-available relational possibilities become relevant and ultimately participate in the realized meaning composite. In the controlled no-context versus prior-context comparison, the sentence, structural relation, and structurally derived default meaning remained unchanged while additional candidate relations became relevant, passed the bounded legitimation process, and participated in the final composite. Additional information can also become relevant without necessarily becoming a participating meaning relation, because legitimation/refusal remains a separate boundary.

The observation reinforces the working S2M view that realized meaning in the current TS model is carried by relationships that participate in the realized composite, rather than by candidate information merely being available to the system.

Central distinction:

available relation ≠ relevant relation ≠ participating relation

Legitimation/refusal sits between relevance and participation.

**What remained invariant**  
- the original structural relation remained unchanged  
- the structurally derived default meaning remained unchanged  
- candidate relations already existed before contextual activation  
- contextual/category processing affected the extension/participation layer rather than rewriting the default

**What was NOT established**  
Experiment 1 did not establish:
- that simultaneously participating relations interact with one another  
- that their combination produces emergent properties  
- that the default relation itself was transformed into a contextualized $R'$  
- that the current exact-tuple licensed-region scaffold is a generalized semantic-licensing mechanism  
- that the TS realization explains biological meaning  
- that relational participation equals subjective experience  
- that it establishes feeling, consciousness, or human-like knowing  
- that this relational mechanism universally explains meaning

The observed refusal behavior is dependent upon the current bounded licensing scaffold and should not be overinterpreted as generalized semantic judgment.

**Methodological result**  
Experiment 1 demonstrates that the current TS realization permits relational meaning formation to be treated as an experimental object whose intermediate states can be exposed, compared, and replayed under controlled conditions.

Methodological proposition (not a confirmed novelty/priority claim): The potential contribution of TS is not the general proposition that meaning is relational. Relational and contextual accounts of meaning have substantial precedent. The potentially distinctive methodological contribution is to make relational meaning formation itself an observable, stage-separated, measurable within the realization, controlled, and replayable object of study.

---

## Experiment 2 — Contextualization of a realized relation

**Status:** Completed at design/observation gate — Gate B

**Experimental question**  
Does additional information merely cause an unchanged candidate relation $R$ to participate, or can the additional information contribute to a distinguishable realized $R'$?

Alternatives:
- Selection/participation alternative: $R + C \rightarrow P(R)$, where $P(R)$ means participation of the unchanged relation $R$.  
- Contextualization alternative: $R + C \rightarrow R'$, where $R'$ must be observably distinguishable from $R$ at the represented relation level.

Experiment 1 established contextual effect on participation. Experiment 2 asked whether the relation itself is observably changed.

**Operational definitions used**
- $R = \text{book} \xrightarrow{\text{is}} \text{object}$  
  - `from = book`  
  - `relation = is`  
  - `to = object`  
  - `major = physical`  
  - `subcategory = natural-kind`  
  - Exists pre-activation in `candidate_interpretations`.
- $C$: prior-context condition `"That location needs support for the object."`
  - Observable path: prior context → CEx/CE → ISc → Merge/TPU → `TP.semantic.isc_category_result` → IdOB/S2M.
- $P(R)$: participation of unchanged $R$ in realized meaning.
  - Operational path observed: `candidate_unselected` → candidate relevance/consideration → `legitimized` → written to `meaning_relations`.
- $R'$ (experimental alternative): relation observably distinguishable from $R$ because contextual information is represented as part of relation identity or relation-level attributes.
  - No such relation-level distinguishing field is exposed in the present realization.

**Controlled comparison**
- Control: sentence `"The book is on the table."`, no prior context.
  - Candidate $R$: `selection_state = candidate_unselected`.
  - $R$ not written to `meaning_relations`.
- Context condition: same sentence, prior context active.
  - Candidate $R$: `selection_state = legitimized`.
  - Written relation: `book → is → object`, `major: physical`, `subcategory: natural-kind`, `legitimized: true`.

**Observed field comparison ($R$ before/after participation)**
- `from`: unchanged  
- `relation`: unchanged  
- `to`: unchanged  
- `major`: unchanged  
- `subcategory`: unchanged  
- No context-, cue-, or provenance-bearing field was added to the written relation object itself.

**Where context remained observable**
- `cue_state.category_cue`
- `cue_state.provenance`
- committed `TP.semantic.isc_category_result`
- category cue/scoring/rationale/provenance fields in that committed block

Distinction recorded:
- Observed: context causally affected whether $R$ participated.
- Not observed: context becoming part of the represented identity of $R$.

**Replay / determinism (tested conditions)**
- control replay identical: `true`
- context replay identical: `true`

**Observed**
- $R$ existed before contextual activation.
- Context was independently observable through the category path.
- Context changed the participation path of $R$.
- $R$ became legitimized in the context condition and entered `meaning_relations`.
- Identity-bearing relation fields of $R$ remained unchanged.
- No relation-level context/provenance qualifier was written into $R$.
- Control/context observations replayed identically under identical tested conditions.

**Interpretation**
Within the current realization, context changed participation of the relation, not its observably represented relational identity. This supports $R + C \rightarrow P(R)$ within the current observation capability.

**Not established**
Experiment 2 does not establish:
- that $R'$ is impossible;
- that context cannot affect relational identity in another representation/realization;
- that future contextual/provenance fields would by themselves prove $R'$;
- that biological contextual meaning behaves this way;
- that participation exhausts contextual meaning;
- that the current relation representation contains every property relevant to realized meaning.

**Conjecture / future question**
Would a future realization expose an operationally meaningful contextual qualification of a relation that is more than participation status or causal history?

**Scaffolding dependencies**
This result is bounded by the current realization and depends on candidate YAML inventories, category-cue mapping, ISc weights, candidate-relevance policy, bounded `LICENSED_EXTENSIONS`, and canonical seed scaffolding.

**Artifacts**
Planned Experiment 2 text artifacts were not created because the experiment completed at the design/observation gate (Gate B). No additional run artifacts were required for this record.

**Contract violations**
No contract violation was identified by Experiment 2. Gate B is a representational-capability observation, not a defect claim.

**Bounded conclusion**
Experiment 2 found that the current TS realization observably supports $R + C \rightarrow P(R)$. Prior contextual information can change whether an already-available relation participates in realized meaning, while the observable identity-bearing fields of that relation remain unchanged. The current instrument therefore does not provide evidence for a distinguishable contextualized relation $R'$.

This does not establish that contextualization of a relation is impossible, nor that contextual information has no effect beyond participation in a more complete realization. It establishes only that the present TS observation instrument does not expose an $R'$ distinguishable from $R$ at the represented relation level.

---

## Experiment 3 — Relational configuration

**Status:** Conditional / planned

Following the Experiment 2 Gate B result, Experiment 3 remains conditional and requires separate review of whether its interaction/configuration distinction is operationally observable with the present instrument.

This experiment should be performed only if the results and instrumentation of Experiment 2 provide a legitimate basis.

**Question**  
When multiple relations participate simultaneously, do they merely coexist in the finite composite, or does their simultaneous relational configuration affect subsequent relational realization?

Null/coexistence case: $M_t = \{R_1, R_2, R_3\}$. The relations participate together, but the set has no demonstrated effect beyond containing them.

Interaction/configuration possibility (provisional, to be operationalized during design): $F(R_1, R_2) \rightarrow R'_3$ or an equivalent operational formulation.

Do not describe this as emergence unless an experiment later provides evidence warranting that term.

**Present evidence boundary**  
Experiment 1 demonstrated co-participation/addition of relations in the final composite. It did not demonstrate that participating relations interact with one another or generate a new relational property. Experiment 3 represents a new experimental question, not an interpretation of Experiment 1.

(Results structure reserved; findings not populated.)

---

## Phase IV stopping rule

Phase IV is initially bounded to these three experiments:

$E_1 \rightarrow$ review $\rightarrow E_2 \rightarrow$ review $\rightarrow E_3$ if warranted $\rightarrow$ Phase IV closeout

No Experiment 4 is added automatically. If these experiments expose another question, propose it separately after Phase IV closeout. The goal is to avoid an indefinitely expanding experimental phase.

## How to record future experiment results

For Experiment 3 (and any approved follow-on), results will contain:
- Question  
- Control condition  
- Experimental condition  
- Held-constant variables  
- Intentionally changed variable  
- Observable states  
- Replay/determinism result  
- Observed  
- Interpretation  
- Not established  
- Conjecture / future question  
- Contract violations, if any  
- Bounded conclusion

This structure keeps experiments comparable over time.

## Relationship to existing documents

- s2m_relational_proposal.md: conceptual authority for the five-stage S2M model.  
- s2m_program_reference.md: executable S2M contract and definition of Phase III/Phase IV methodology, including the epistemic boundary.  
- user_guide.md: instrument-reading manual.  
- category_selection_proposal.md: bounded category-selection phenomenon and architectural boundaries.  
- This document: experimental protocol and record for the three Phase IV experiments.

Large portions of the authorities are not duplicated; links are provided where appropriate.

## Claim discipline

Language is limited to: observed within the current TS realization; reinforces the working S2M view; supports further investigation; not established; methodological proposition.

Broader conjectures concerning feeling, subjective experience, biological versus silicon experience, experiential knowing, consciousness, or related topics are outside the scope of this bounded Phase IV experiment paper.
