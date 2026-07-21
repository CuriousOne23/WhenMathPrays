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
{\text{snapshot}}_{t}\left(L\right)
$$

These snapshots form the basis for all stability metrics.

## 2. Counting, Frequency, and History
CST Core tracks how often a structural feature fappears across the last 10 turns.

Total count over window

$$
C^{f}\left(L\right)=\sum_{k=t-9}^{t} 1\left[f\in {\text{snapshot}}_{k}\left(L\right)\right]
$$

This counts the number of turns in which feature fappears.

Frequency over window

$$
F^{f}\left(L\right)=\frac{C^{f}\left(L\right)}{10}
$$

This normalizes the count to a 0–1 frequency.

Ordered reference history

$$
H^{f}\left(L\right)=\left(h_{t-9},\ h_{t-8},\ \ldots ,\ h_{t}\right)
$$

where each $h_{k}$ encodes the presence, strength, or importance of feature fat turn k.
