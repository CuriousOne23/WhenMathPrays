### 1. Numbered List of Tests
The test suite covers all layers with focused, layered validation.

**OuBA Tests**  
1.1 SSR field weighting  
1.2 SSR boundary conditions  
1.3 SSR → coordinate mapping (from ssr_to_manifold_transfer_guide.md and related)

**Manifold Tests**  
2.1 Attractor basin identification  
2.2 Curvature invariants  
2.3 Spline-fit constraints  
2.4 φ_G semantic-shape behavior (from manifold white papers)

**Projection Tests**  
3.1 Dictionary rule activation  
3.2 Routing logic  
3.3 Projection invariants (from dictionary_projection_spec.md and related)

**OuBB Tests**  
4.1 Tone/intent realization  
4.2 Surface-form correctness  
4.3 Reversibility (OuBB → manifold → OuBA)

**Integration Tests**  
5.1 Full AB-suite behavior  
5.2 Drift detection  
5.3 Invariant preservation across layers

### 2. Numeric Outputs for Each Test
Defined outputs align with the numeric policy and data structures in the requirements.

- **SSR numeric output** (OuBA): SSR fields in [0,1], weighted SSR vector, coordinate mapping (x,y,z) or equivalent.  
- **Manifold numeric output**: Attractor distance, curvature value, spline deviation, basin stability score.  
- **Projection numeric output**: Rule activation vector, routing confidence, projection error score.  
- **OuBB numeric output**: Tone score, intent score, reversibility drift.  
- **Integration numeric output**: End-to-end consistency metrics (e.g., composite drift, invariant match scores).

### 3. Good vs. Bad Numeric Thresholds
Thresholds are set for pass/fail criteria, drawing from stability, invariance, and validation requirements.

**SSR thresholds**  
- Good: mapping error ≤ 0.03  
- Bad: mapping error > 0.05  

**Manifold thresholds**  
- Good: attractor distance ≤ 0.10; curvature deviation ≤ 0.05; basin stability score ≥ 0.90  
- Bad: attractor distance > 0.20; curvature deviation > 0.10; basin stability score < 0.75  

**Projection thresholds**  
- Good: rule activation matches attractor signature ≥ 0.85; projection error ≤ 0.05; routing confidence ≥ 0.90  
- Bad: rule activation < 0.70; projection error > 0.10; routing confidence < 0.75  

**OuBB thresholds**  
- Good: tone/intent match ≥ 0.90; reversibility drift ≤ 0.05  
- Bad: tone/intent match < 0.75; reversibility drift > 0.10  

**Integration thresholds**  
- Good: composite drift ≤ 0.05; invariant preservation ≥ 0.95  
- Bad: composite drift > 0.10; invariant preservation < 0.85  

### 4. Requirement(s) Validated by Each Test
Mapping ties directly to HLRs, primitives, and specs in the 20-series and system_playground.

- **OuBA/SSR tests** validate: SSR field definitions, numeric boundaries, transfer guide rules (ssr_to_manifold_transfer_guide.md and OuBA primitives).  
- **Manifold tests** validate: φ_G semantic shape definitions, basin stability, spline constraints, manifold geometry papers, and related invariants.  
- **Projection tests** validate: Dictionary rule attachment, routing invariants, projection correctness (dictionary_projection_spec.md, routing specs).  
- **OuBB tests** validate: Surface-form generation, tone/intent realization, reverse projection invariants (OuBB assembly rules, examples).  
- **AB integration tests** validate: Cross-layer stability, drift control, end-to-end reversibility, overall pipeline specs, and invariants from architecture documents.

### 5. Structured Outline for the Paper `ts_e2e_logic_sim_01.md`
**1. Purpose**  
High-level goal of the end-to-end logic simulation for validation of the TS pipeline.

**2. Requirements Referenced**  
Summary of key documents from `20_requirements/` and `system_playground/` (SSR transfer guide, dictionary projection spec, manifold geometry/white papers, OuBB examples, etc.).

**3. Test Suite Overview**  
Numbered list of tests with layer coverage.

**4. Numeric Output Definitions**  
Detailed per-layer outputs as defined above.

**5. Good/Bad Thresholds**  
Threshold tables with rationale tied to numeric policy and stability requirements.

**6. Test-by-Test Requirement Mapping**  
Explicit links to validated HLRs/requirements.

**7. Expected Invariants**  
Cross-layer preservation expectations (e.g., semantic shape, reversibility, drift bounds).

**8. Next Steps (Execution Phase)**  
Guidance for running the simulation in a subsequent step, including execution order, input selection, logging, and post-run analysis.

