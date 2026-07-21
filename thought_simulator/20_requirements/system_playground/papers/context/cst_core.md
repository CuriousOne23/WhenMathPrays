# CST Core: Context Stability Tracking — Core Specification  

CST Core is the foundational stability module in the Thought Simulator system. Its purpose is to track, quantify, and stabilize structural identity signals across turns, ensuring continuity, preventing collapse, and enabling deterministic recovery.

CST Core monitors:
- identity structure
- referent structure
- temporal anchors
- discourse anchors
- lineage continuity
- register state
- field importance stability

It computes metrics over a 10 turn sliding window, producing drift, oscillation, ambiguity, collapse, and stability signals that feed into higher level CST modules (CST MS, CST Mux, CST CIL, etc.).

## 1. Structural Snapshots  
At each turn t, CST Core extracts a snapshot of structural features for each identity layer L. A snapshot may include:
- referent map
- temporal anchor positions
- discourse anchor positions
- lineage connections
- register state
- field importance weights

Snapshots are stored as:

$$
{\text{snapshot}}_{t}(L)
$$

These snapshots form the basis for all stability metrics.

## 2. Counting, Frequency, and History  
CST Core tracks how often a structural feature fappears across the last 10 turns.

Total count over window

$$
C^{f}(L)=\sum_{k=t-9}^{t} 1[f\in {\text{snapshot}}_{k}(L)]
$$

This counts the number of turns in which feature fappears.

Frequency over window

$$
F^{f}(L)=\frac{C^{f}(L)}{10}
$$

This normalizes the count to a 0–1 frequency.

Ordered reference history

$$
H^{f}(L)=(h_{t-9},\ h_{t-8},\ \ldots ,\ h_{t})
$$

where each $h_{k}$ encodes the presence, strength, or importance of feature fat turn k.

## 3. Drift Detection  
CST Core computes drift metrics for identity, referent, temporal, discourse, lineage, and register structures. Drift measures how much a structural feature changes from one turn to the next, and whether those changes accumulate enough to threaten stability.

Let $x_{t}^{(L)}$ be the structural feature vector for layer Lat turn t. This vector may encode:
- referent distribution
- anchor positions
- lineage connections
- register state
- field importance weights
- any other structural signals tracked by CST Core

**Per turn drift**  
Drift at a single turn compares the structure at turn tto the structure at turn t-1:

$$
D(L,\ t)=d(x_{t}^{(L)},x_{t-1}^{(L)})
$$

Here:
- $d(\cdot ,\ \cdot)$ is a deterministic structural distance function
- No randomness or sampling is allowed
- The distance function is chosen per metric type

Examples of valid distance functions:
- set difference
- ordering distance
- weighted field difference
- referent map mismatch
- lineage edge change count

**Integrated drift over window**  
CST Core integrates drift over the last 10 turns to detect sustained instability:

$$
\bar{D}(L)=\frac{1}{10}\sum_{k=t-9}^{t} D(L,\ k)
$$


This produces a normalized drift score between 0 and the maximum possible structural distance.

If $\bar{D}(L)$ exceeds a drift threshold, CST Core emits a drift signal for layer L.

**Distance function specification**  
The distance function $d(\cdot ,\ \cdot)$ is deterministic and metric specific:
- identity_drift Measures change in overall identity structure.
- referent_drift Measures change in referent map (e.g., referent reassignment, disappearance, or instability).
- lineage_drift Measures change in lineage connections (e.g., parent/child structural links).
- register_drift Measures change in register state (e.g., formal/informal, tense, modality).

Each metric uses a distance function appropriate to its structural domain.

**Threshold comparison**  
CST Core compares integrated drift against monotonic thresholds:

$$
\bar{D}(L)\gt {\theta }_{\text{drift}}(L)
$$

If this condition is true, CST Core emits a drift signal for layer L.
Thresholds are:
- deterministic
- monotonic
- layer specific
- updated only through CST Core’s threshold update rules (Section 10)

## 4. Oscillation Detection  
Oscillation measures how often a structural feature flips state across the 10 turn window. Where drift measures magnitude of change, oscillation measures frequency of change.

Oscillation is important because:
- high oscillation = instability
- low oscillation = continuity
- zero oscillation = fully stable structure

Let $s_{k}^{(L)}$ be the state of feature fat turn kfor layer L. A “state” may be:
- referent assignment
- anchor position
- lineage link
- register mode
- field importance classification
- any discrete structural signal CST Core tracks

**Oscillation score**  
Oscillation counts the number of times the state changes between consecutive turns:

$$
O^{f}(L)=\sum_{k=t-9}^{t-1} 1[s_{k}^{(L)}\neq s_{k+1}^{(L)}]
$$

This uses the indicator function:
- $1[\text{condition}]= 1$ if the condition is true
- $1[\text{condition}]= 0$ otherwise

So each time the state flips, oscillation increments by 1.

**Interpretation**  
-	O = 0 No oscillation. The feature is stable.
-	O = 1–2 Mild oscillation. Acceptable for dynamic structures.
-	O = 3–5 Moderate oscillation. CST Core may begin monitoring for collapse.
-	O ≥ 6 High oscillation. CST Core emits an oscillation warning.

Oscillation is layer specific, so each identity layer Lhas its own oscillation score.

**Threshold comparison**  
CST Core compares oscillation against a monotonic threshold:

$$
O^{f}(L)\gt {\theta }_{\text{osc}}(L)
$$

If true, CST Core emits an oscillation signal for layer L.

Thresholds are:
-	deterministic
-	monotonic
-	updated only through CST Core’s threshold update rules

**Why oscillation matters**  
Oscillation is one of the earliest indicators of structural instability. Even if drift is low (small changes), frequent flipping can destabilize:
-	referent continuity
-	temporal anchoring
-	discourse structure
-	lineage consistency
-	register coherence

Oscillation often precedes collapse, so CST Core treats it as a high priority signal.

## 5. Ambiguity Detection  
Ambiguity measures how uncertain, unstable, or overlapping a structural feature’s interpretation becomes across the 10 turn window. Where drift measures change, and oscillation measures flipping, ambiguity measures confusion.

Ambiguity arises when:
-	referents become unclear
-	temporal anchors overlap or contradict
-	discourse anchors lose clarity
-	lineage connections become ambiguous
-	register signals conflict
-	field importance weights become unstable

Let $A^{f}(L,\; t)$ be the ambiguity score for feature fat turn tfor layer L.

**Per turn ambiguity**  
Each turn produces an ambiguity score:

$$
A^{f}(L,\ t)
$$

This score is computed by the metric specific ambiguity function, which may consider:
-	referent overlap
-	anchor collision
-	lineage uncertainty
-	register conflict
-	field importance instability

The exact ambiguity function is deterministic and domain specific.

**Integrated ambiguity over window**  
CST Core integrates ambiguity over the last 10 turns:

$$
{\bar{A}}^{f}(L)=\frac{1}{10}\sum_{k=t-9}^{t} A^{f}(L,\ k)
$$

This produces a normalized ambiguity score between 0 and the maximum ambiguity allowed by the metric.

**Interpretation**  
-	$\bar{A}=0$ No ambiguity. Structure is fully clear.
-	$\bar{A}=0.1\text{-}0.3$ Mild ambiguity. Acceptable for dynamic contexts.
-	$\bar{A}=0.4\text{-}0.6$ Moderate ambiguity. CST Core begins monitoring for collapse.
-	$\bar{A}\geq 0.7$ High ambiguity. CST Core emits an ambiguity warning.

Ambiguity is feature specific and layer specific.

**Threshold comparison**  
CST Core compares integrated ambiguity against a monotonic threshold:

$$
{\bar{A}}^{f}(L)\gt {\theta }_{\text{amb}}(L)
$$

If true, CST Core emits an ambiguity signal for layer L.

Thresholds:
-	are deterministic
-	are monotonic
-	evolve only through CST Core’s threshold update rules
-	differ per identity layer

**Why ambiguity matters**  
Ambiguity is one of the strongest predictors of collapse. Even if drift is low and oscillation is moderate, high ambiguity indicates that the system cannot reliably interpret structural signals.

Ambiguity often precedes:
-	referent collapse
-	temporal collapse
-	discourse collapse
-	lineage collapse
-	register collapse

Thus CST Core treats ambiguity as a critical stability metric.

## 6. Collapse Detection  
Collapse is CST Core’s strongest instability signal. Where drift measures change, oscillation measures flipping, and ambiguity measures confusion, collapse measures structural failure — the point at which continuity cannot be maintained without intervention.
Collapse is computed from stability metrics. Let S^{f}(L,\; t\right)be the stability score for feature fat turn tfor layer L.
Stability scores are domain specific and may incorporate:
	referent continuity
	temporal anchor persistence
	discourse anchor coherence
	lineage link stability
	register consistency
	field importance stability
CST Core integrates stability over the 10 turn window.
Integrated stability over window
{\bar{S}}^{f}(L\right)=\frac{1}{10}\sum_{k=t-9}^{t} S^{f}(L,\; k\right)

This produces a normalized stability score between 0 and 1.
	\bar{S}=1→ fully stable
	\bar{S}=0→ fully collapsed
	intermediate values → partial stability
Collapse score
Collapse is defined as the complement of stability:
C^{f}(L\right)=1-{\bar{S}}^{f}(L\right)

Interpretation:
	C=0→ no collapse
	C=0.1–0.3→ mild instability
	C=0.4–0.6→ moderate collapse risk
	C≥0.7→ high collapse risk
	C=1→ full collapse
Collapse is feature specific and layer specific.
Threshold comparison
CST Core compares collapse against a monotonic threshold:
C^{f}(L\right)\gt {\theta }_{\text{collapse}}(L\right)

If true, CST Core emits a collapse signal for layer L.
Thresholds:
	are deterministic
	are monotonic
	differ per identity layer
	evolve only through CST Core’s threshold update rules
Why collapse matters
Collapse is the most severe stability signal. It indicates that the system can no longer maintain continuity without corrective action.
Collapse often triggers:
	freeze (Section 7)
	thaw gating (Section 8)
	continuity restoration (Section 9)
	threshold adaptation (Section 10)
Collapse is the point where CST Core must intervene to prevent structural failure.
Continuing exactly as requested — Section 7, fully rendered in chat, clean math, no GitHub assumptions, no agent involvement, and not pulling from your open tabs. We stay entirely inside the CST Core white paper.
7. Freeze Detection
Freeze is CST Core’s emergency stabilization mechanism. When drift, oscillation, ambiguity, or collapse exceed safe limits, CST Core may freeze a structural layer to prevent further degradation.
Freeze is not collapse. Freeze is a protective action that halts structural updates until stability can be restored.
Freeze is triggered when:
	collapse is high
	ambiguity is high
	oscillation is high
	drift is high
	continuity is threatened
	stability cannot be guaranteed
Freeze ensures that the system does not continue updating a layer that is already unstable.
Freeze condition
Let C_{\text{total}}(L\right)be the combined instability score for layer L. This score is computed from:
	drift
	oscillation
	ambiguity
	collapse
CST Core triggers freeze when:
C_{\text{total}}(L\right)\gt {\theta }_{\text{freeze}}(L\right)

Interpretation:
	Below threshold → layer continues updating normally
	Above threshold → layer freezes immediately
Freeze is layer specific and does not affect other layers unless their own thresholds are exceeded.
What freeze does
When a layer freezes:
	Snapshots stop updating {\text{snapshot}}_{t}(L\right)is held constant.
	Stability metrics stop updating Drift, oscillation, ambiguity, and collapse are paused.
	Thresholds stop adapting Threshold evolution halts for that layer.
	Continuity is preserved The layer cannot degrade further.
Freeze is a hard stop on structural evolution.
Why freeze matters
Freeze prevents:
	referent collapse
	temporal collapse
	discourse collapse
	lineage collapse
	register collapse
	field importance collapse
Freeze is the system’s last line of defense before structural failure.
Freeze duration
Freeze persists until thaw conditions are met (Section 8). Freeze is not time based; it is condition based.
A layer remains frozen until:
	collapse decreases
	ambiguity decreases
	oscillation decreases
	drift decreases
	stability improves
	continuity is restored
Only then can thaw occur.
Continuing exactly as requested — Section 8, fully rendered in chat, clean math, no GitHub assumptions, no agent involvement, and not pulling from your open tabs. We stay entirely inside the CST Core white paper.
8. Thaw Detection
Thaw is the controlled reversal of freeze. Where freeze halts structural updates to prevent collapse, thaw restores normal operation once stability returns.
Thaw is never time based. Thaw is strictly condition based.
A layer remains frozen until CST Core determines that:
	collapse has decreased
	ambiguity has decreased
	oscillation has decreased
	drift has decreased
	stability has improved
	continuity is safe again
Only then can thaw occur.
Thaw condition
Let C_{\text{total}}(L\right)be the combined instability score for layer L. Thaw occurs when instability falls below a recovery threshold:
C_{\text{total}}(L\right)\leq {\theta }_{\text{recover}}(L\right)

Interpretation:
	Above threshold → layer remains frozen
	Below threshold → layer thaws and resumes normal updates
Thaw thresholds are:
	deterministic
	monotonic
	layer specific
	distinct from freeze thresholds
	updated only through CST Core’s threshold update rules
What thaw does
When thaw occurs:
	Snapshots resume updating {\text{snapshot}}_{t}(L\right)begins capturing new structural states again.
	Stability metrics resume updating Drift, oscillation, ambiguity, and collapse calculations restart.
	Thresholds resume adapting Layer specific thresholds begin evolving again.
	Continuity restoration begins The layer re enters normal structural evolution.
Thaw is a soft restart of structural dynamics.
Why thaw matters
Thaw ensures that freeze is not permanent. Freeze protects stability, but thaw restores flexibility.
Without thaw:
	layers would remain frozen indefinitely
	structural evolution would halt
	referent continuity could stagnate
	temporal anchors could become outdated
	discourse structure could become rigid
	lineage and register signals could fail to adapt
Thaw ensures that CST Core can recover from instability and resume normal operation.
Freeze–thaw cycle
The freeze–thaw cycle is central to CST Core’s stability model:
	Freeze prevents collapse.
	Thaw restores continuity.
	Thresholds govern transitions.
	Metrics determine when transitions occur.
This cycle ensures deterministic, safe, and adaptive structural behavior.

9. Continuity Restoration
Continuity restoration is CST Core’s mechanism for rebuilding structural stability after instability, freeze, or collapse. Where freeze protects a layer from further degradation, continuity restoration repairs the layer so it can safely resume normal evolution.
Continuity restoration is triggered when:
	drift decreases
	oscillation decreases
	ambiguity decreases
	collapse decreases
	lineage continuity improves
	register stability improves
	field importance stability improves
CST Core uses continuity restoration to ensure that structural signals return to a coherent, deterministic state.
Continuity score
Let K(L,\; t\right)be the continuity score for layer Lat turn t. This score measures how well the structure at turn taligns with the structure at turn t-1.
Examples of continuity domains:
	lineage continuity
	identity continuity
	referent continuity
	temporal continuity
	discourse continuity
	register continuity
Integrated continuity over window
CST Core integrates continuity over the last 10 turns:
\bar{K}(L\right)=\frac{1}{10}\sum_{k=t-9}^{t} K(L,\; k\right)

Interpretation:
	\bar{K}=1→ perfect continuity
	\bar{K}=0.7\text{-}0.9→ strong continuity
	\bar{K}=0.4\text{-}0.6→ moderate continuity
	\bar{K}\lt 0.3→ continuity failure
Continuity is layer specific.
Continuity restoration condition
CST Core restores continuity when:
\bar{K}(L\right)\geq {\theta }_{\text{cont,recover}}(L\right)

If true:
	thaw becomes possible (Section 8)
	freeze can be lifted
	structural updates resume
	queued corrections can be applied
	stability metrics restart normally
Continuity restoration is the gateway to thaw.
What continuity restoration does
When continuity restoration is active:
	Structural corrections are applied Merge, split, retire, weaken, strengthen signals queued during freeze are executed deterministically.
	Snapshots resume normal evolution {\text{snapshot}}_{t}(L\right)begins updating again.
	Stability metrics restart Drift, oscillation, ambiguity, collapse, and register metrics resume.
	Thresholds resume adapting Layer specific thresholds begin evolving again.
	Identity coherence is rebuilt The layer returns to a stable structural trajectory.
Continuity restoration is the system’s recovery phase.
Why continuity restoration matters
Without continuity restoration:
	freeze would be permanent
	layers would stagnate
	identity evolution would halt
	referent and anchor structures would become outdated
	lineage and register signals would fail to adapt
	collapse recovery would be impossible
Continuity restoration ensures that CST Core can repair, recover, and resume deterministic structural behavior.
10. Determinism, Thresholds, and Replay
CST Core is governed by strict determinism rules. All metrics, thresholds, and signals must be reproducible, replay safe, and independent of external state. This ensures that identity layer evolution is fully deterministic, even across long horizons.
Determinism is enforced through:
	pure functional metrics
	monotonic thresholds
	replay safe update rules
	no randomness
	no wall clock time
	no external state
	complete logging of metric history
These constraints guarantee that CST Core behaves identically under replay, simulation, or long horizon analysis.
10.1 Deterministic Metric Functions
Every CST Core metric is a pure function of:
	the COB snapshot
	OuBA cues
	previous CST signals
	deterministic metric history
Formally, for any metric M:
M_{t}=f({\text{snapshot}}_{t},\; {\text{OuBA}}_{t},\; {\text{CST}}_{t-1},\; \text{history}\right)

There is no randomness, no sampling, and no external state.
This ensures:
	replay consistency
	deterministic evolution
	predictable stability behavior
	safe long horizon integration
10.2 Monotonic Thresholds
Thresholds evolve deterministically according to monotonic update rules.
Let {\theta }_{t}be a threshold at turn t. Thresholds update according to:
{\theta }_{t+1}=g({\theta }_{t},\; \text{metric\ history}\right)

Where:
	gis deterministic
	thresholds never decrease unless explicitly allowed
	thresholds never increase unless explicitly allowed
	thresholds remain within bounded ranges
	thresholds are replay safe
Each layer Lhas its own threshold set:
	drift threshold
	oscillation threshold
	ambiguity threshold
	collapse threshold
	freeze threshold
	thaw/recovery threshold
	continuity threshold
	register stability threshold
	field importance stability threshold
Thresholds ensure that CST Core reacts consistently to structural changes.
10.3 Replay Safety
Replay safety means that CST Core produces identical outputs when given identical inputs and history.
Replay safety requires:
	deterministic metric functions
	deterministic threshold updates
	deterministic freeze/thaw logic
	deterministic collapse logic
	deterministic signal ordering
	complete logging of metric values
Replay safety is essential for:
	debugging
	long horizon analysis
	identity layer evolution
	deterministic merge/split behavior in CST MS
	deterministic signal aggregation in CST Mux
10.4 Deterministic Signal Ordering
CST Core emits signals in a deterministic order:
	drift
	oscillation
	ambiguity
	collapse
	continuity
	freeze
	thaw
	register stability
	field importance stability
Signal ordering ensures:
	no race conditions
	no ambiguous behavior
	deterministic downstream processing
	safe integration with CST MS and CST Mux
10.5 Summary of Determinism Guarantees
CST Core guarantees:
	deterministic metric computation
	deterministic threshold evolution
	deterministic freeze/thaw behavior
	deterministic collapse detection
	deterministic continuity restoration
	deterministic register and field importance stability
	deterministic replay across identity layer evolution
These guarantees make CST Core the foundation of the CST architecture.


