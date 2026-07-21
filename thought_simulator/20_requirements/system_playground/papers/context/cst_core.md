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

Continuing exactly as requested — Section 4, fully rendered in chat, clean math, no GitHub assumptions, no agent involvement, no pulling from your tabs. This is the next section of the CST Core white paper.

