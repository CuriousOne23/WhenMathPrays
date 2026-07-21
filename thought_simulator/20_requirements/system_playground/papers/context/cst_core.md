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
