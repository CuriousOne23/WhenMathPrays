# Primitive Modeling Guide: M1/M2 Perspective Framework

## Table of Contents

1. [Axis Mapping Foundation](#axis-mapping-foundation)
2. [Identity Statement Test](#identity-statement-test-distinguishing-real-vs-imaginary-primitives)
3. [Primitive Definitions & Scoring Rules](#primitive-definitions--scoring-rules)
4. [Common Patterns](#common-patterns)
5. [Example: The Notebook – Allie’s Perspective](#example-the-notebook--allies-perspective-gamma_self--allie-other--noah)
6. [The Double Projection Problem](#the-double-projection-problem)
7. [Critical Distinction](#critical-distinction)
8. [The Framework](#the-framework)
9. [Key Insight: Fidelity Direction](#key-insight-fidelity-direction)
10. [Examples](#examples)
11. [Common Pitfalls](#common-pitfalls)
12. [Validation Checklist](#validation-checklist)
13. [Edge Cases](#edge-cases)
14. [Quick Reference Table](#quick-reference-table)
15. [Documentation Best Practice](#documentation-best-practice)
16. [Summary](#summary)

**⚠️ CRITICAL:** This framework is counterintuitive. Read carefully and reference often. Even after understanding it, the natural human tendency is to slip back into incorrect "theory-of-mind" scoring.

---

## Axis Mapping Foundation

The GRP framework rests on a specific mapping of primitives to axes:

**Real Axis (Ego ↔ We): Identity Boundary**
- **Visibility (v)**: Showing up vs hiding affects connection/separation (structural dimension)
- **Interpretation**: The Real axis represents **identity boundary** or identity merger:
  - **Ego-space (Real negative)**: Separate, distinct identities—M1 experiences self as "I" (distinct from M2)
  - **We-space (Real positive)**: Merged, shared identity—M1 experiences self as "We" (self-concept includes M2)

**Imaginary Axis (Hate ↔ Love): Affective Quality**
- **Resonance (r)**: Emotional attunement vs discord affects affective quality
- **Fidelity (f)**: Trust vs betrayal affects love/hate trajectory
- **Altruism (a)**: Generosity vs selfishness affects positive/negative sentiment
- **Interpretation**: The Imaginary axis represents **emotional experience** or affective states—how M1 feels about M2

**Both Axes:**
- **Shared Breath (S)**: Concrete togetherness affects both connection AND affect

**Polarity Principle:**
- **Positive values** push toward We+Love
- **Negative values** push toward Ego+Hate
- **Negative ≠ absence** - it means opposite action/state

For detailed research foundation defending these mappings, see [Axis Mapping Validation](../gamma_self_defense.md#axis-mapping-validation-why-these-primitives-map-to-these-axes) in gamma_self_defense.md.

### Identity Statement Test: Distinguishing Real vs Imaginary Primitives

A practical linguistic test for classifying primitives:

**Imaginary Axis Primitives (r, f, a):** Use **action** or **feeling** language
- "I helped them" (action, identity remains distinct)
- "I care about them" (feeling, identity remains distinct)
- "I resonate with them" (emotional experience)
- "I am faithful to them" (describes commitment action/feeling)

**Real Axis Primitives (v):** Can support **identity** language
- "I am married to them" (defines WHO M1 is)
- "We are partners" (shared identity statement)
- "This is my spouse" (possessive identity incorporation)
- "We are buying a house" (joint identity action)

**Key Distinction:**
- **Imaginary effects** describe what M1 **DOES** or **FEELS** toward M2—M1's identity remains distinct
- **Real effects** define WHO M1 **IS** in relation to M2—M1's self-concept incorporates M2

**Examples:**
- **Fan relationship**: "I love this celebrity" (Imaginary: Love) + "They don't know I exist" (Real: Ego-space)—high r/a doesn't create identity merger
- **Charity**: "I donated to this cause" (Imaginary: high a) + "I am not part of them" (Real: Ego-space)—altruism without identity merger
- **Marriage**: "I feel distant from my spouse" (Imaginary: Hate) + "I am married to them" (Real: We-space)—identity merger persists despite negative affect
- **Toxic enmeshment**: "I resent them" (Imaginary: Hate) + "I can't be without them" (Real: We-space)—negative affect with identity dependence

This test helps prevent misclassifying primitives: r/a/f affect how M1 **feels**, while v affects whether M1's **identity** incorporates M2.

---

# Generalized Relational Physics (GRP) – Primitive Scoring Guidelines

These guidelines define how to score the five primitives (v, r, f, a, S) in scenario CSV files.  
Each primitive value must reflect **only gamma_self's internal emotional response inspired by the other person** at that exact moment/event — never the other person's feelings, never an objective "relationship quality" average.

Scale: -10 (maximum negative) to +10 (maximum positive), 0 neutral.

## Core Principles

1. **Subjectivity Rule**  
   Score from gamma_self's viewpoint only: "What feelings does the other person arouse *in me* right now?"

2. **Asymmetry is Normal**  
   One party can feel maximum positives while the other feels negatives or neutrals (e.g., Noah instantly high on Allie; Allie initially wary/low).

3. **Primitives are Independent**  
   High resonance does not require high altruism. Shared breath can be maximum while visibility is negative.

## Primitive Definitions & Scoring Rules

| Primitive | Meaning | Positive High (+8 to +10) | Neutral (–2 to +2) | Negative High (–8 to –10) | Key Scoring Notes |
|-----------|---------|---------------------------|---------------------|----------------------------|-------------------|
| **v**<br>Visibility | How much the other dominates my perceptual/emotional field, and whether I *desire* that presence | They are constantly in my thoughts; I crave their presence; I can't look away | They are present but not dominating; I neither seek nor avoid them strongly | Their presence feels intrusive, overwhelming, or unwanted; I want distance | Negative v = "Get out of my sight/head"<br>Positive v = "You fill my entire world" |
| **r**<br>Resonance | Degree of deep harmonic alignment / soul-level sync | Perfect harmony; we vibrate on the same frequency; everything feels "right" | Mild connection or neutral vibe | Dissonance; their energy clashes with mine | Often flips quickly in love stories once the spark lands |
| **f**<br>Fidelity | Trust, faith, and loyalty inspired in me toward them/the bond | Complete trust; unwavering belief in them and our connection | Neither strong trust nor distrust | Doubt, suspicion, or sense of betrayal | Can remain high through absence if faith persists |
| **a**<br>Altruism | Desire to act for *their* benefit/flourishing (not my own need) | I want to give to them selflessly; their happiness matters more than my comfort | Mild or no particular wish to help/harm them | I wish them ill or feel indifference to their well-being | **Lags behind other primitives** — requires actually *knowing* the person to rise significantly<br>Early passion is usually low a (driven by own desire) |
| **S**<br>Shared Breath | Sense of mutual purpose, shared story, breathing the same air | We live in the same dream; complete alignment of life direction | Purposes neither strongly aligned nor opposed | Divergent or opposing purposes; one-sidedness feels rejecting | Drops fast in separation; negative when the other feels like an obstacle to my path |

## Common Patterns

- **Early resistance (reluctant party)** → negative or low v, r, S, f; a usually 0 or low positive if they feel delighted despite resistance.
- **Pursuit phase** → pursuer often high v/r/f/S, low a (driven by own need).
- **Peak passion** → high r, f, S; v usually high; a still moderate until deeper knowledge forms.
- **Separation/conflict** → v drops, S drops first, a and f can linger positive if love persists.
- **Transcendent/enduring love** → maximum scores reserved for tested moments (e.g., lucid recognition in illness, lifelong sacrifice).

## Example: The Notebook – Allie’s Perspective (gamma_self = Allie, other = Noah)

| Day | Event                          | v   | r   | f   | a   | S   | Rationale |
|-----|--------------------------------|-----|-----|-----|-----|-----|-----------|
| 0   | First sighting at carnival     | -2  | -2  | 0   | 0   | -2  | Noah forces attention; feels intrusive and socially mismatched |
| 1   | Ferris wheel dare              | -3  | -3  | -2  | 5   | -1  | Still resistant (negative v/r/f/S), but his boldness delights her (moderate a) |
| 30  | Summer romance peak            | 8   | 10  | 8   | 8   | 10  | Deep harmony and shared dream; strong but not yet total selflessness |
| 365 | Separation & engagement to Lon | 0   | 2   | 3   | 7   | 8   | Noah no longer daily present (v=0); lingering care (high a/S) but muted trust/resonance |
| 730 | Reading the notebook           | 9   | 10  | 9   | 9   | 10  | Memories flood back; full restoration of love and purpose |
| 2555| Alzheimer’s years (lucid moments) | 10 | 10  | 10  | 10  | 10  | In clarity, Noah inspires absolute maximum everything |

Follow these guidelines strictly for any new scenario. Score moment-by-moment from the specified gamma_self's internal experience only.

---

## The Double Projection Problem

This is the most common mistake and the hardest to avoid. It requires constant vigilance.

### Natural (but Wrong) Thought Process

When you think about Romeo and Juliet's relationship, your natural instinct is:

1. **First projection:** "I think about Romeo" (you → Romeo)
2. **Second projection:** "Romeo thinks about Juliet" (Romeo → Juliet)
3. **Natural question:** "What does Romeo think Juliet feels about him?"

This leads to scoring Romeo's **beliefs about Juliet** in Romeo's file.

### Correct (but Unnatural) Thought Process

The framework requires you to ask:

1. **First projection:** "I think about Romeo" (you → Romeo)
2. **Causal question:** "How does Juliet's presence affect Romeo's relational state?"
3. **Phenomenological question:** "What are Romeo's primitives evoked by Juliet?"

This leads to scoring Romeo's **own relational states caused by Juliet** in Romeo's file.

### Concrete Example: The Balcony Scene

**Wrong Approach (Natural but Incorrect):**

Thinking: "Romeo is falling in love. He believes Juliet loves him back. She seems faithful."

Scoring Romeo's file:
```csv
day,v,r,f,a,S
2,10,10,10,9,9  # "Romeo perceives high fidelity from Juliet"
```

❌ This scores Romeo's **theory of mind** about Juliet.

**Correct Approach (Unnatural but Right):**

Thinking: "Juliet's presence evokes maximum engagement in Romeo. Romeo is fully visible, resonating deeply, being completely faithful to her, acting with high agency, and spiritually present."

Scoring Romeo's file:
```csv
day,v,r,f,a,S
2,10,10,10,9,9  # "Romeo's own primitives evoked by Juliet"
```

✅ This scores Romeo's **phenomenological state** caused by Juliet.

**The values might look the same, but the semantics are completely different.**

### Why This Is Hard

The double projection is cognitively natural:
- We naturally model others' mental states
- "Theory of mind" is a fundamental human capability
- Relationships are inherently dyadic (two people thinking about each other)

The framework is phenomenologically grounded:
- It models one person's first-person experience
- "My relational state" not "my beliefs about you"
- Focus is causal (your presence → my state) not cognitive (my beliefs about your beliefs)

**You will constantly slip into theory-of-mind modeling.** When you catch yourself asking "What does M1 believe about M2?", stop and ask "What relational states does M2 evoke in M1?"

### Practical Test

Before scoring any primitive, ask yourself:

**Theory of Mind Question (WRONG):**
- "Does Romeo think Juliet is faithful?"
- "Does Romeo believe Juliet sees him?"
- "Does Romeo perceive resonance from Juliet?"

**Phenomenological Question (RIGHT):**
- "Is Romeo faithful to Juliet?"
- "Is Romeo visible/seeing in relation to Juliet?"
- "Does Romeo resonate with Juliet?"

If you're asking about Romeo's **beliefs**, you've slipped into theory-of-mind.  
If you're asking about Romeo's **relational states**, you're doing it correctly.

## Critical Distinction

**WRONG:** Score primitives from external observer's viewpoint (how WE see M1's behavior)  
**RIGHT:** Score primitives from M1's subjective internal experience of M2's impact on them

## The Double Projection Problem

The framework requires a "double projection" that is unnatural to human thinking:

**Natural human thought (WRONG):**
1. I (observer) think about Romeo (M1)
2. Romeo thinks about Juliet (M2)
3. What does Romeo **believe** Juliet feels about him?

**Framework requirement (CORRECT):**
1. Romeo (M1) experiences Juliet's (M2) presence
2. That presence **evokes** relational states in Romeo
3. What are Romeo's primitives **caused by** Juliet?

### Why This Is Hard

We naturally ask theory-of-mind questions: "What does M1 think M2 thinks?"

The framework asks phenomenological questions: "What relational state does M2's presence evoke in M1?"

**Example - Scoring fidelity at the tomb:**

❌ **Natural (Wrong) Thought Process:**
- "Romeo sees Juliet dead"
- "Romeo wonders: 'Was she faithful to me?'"
- "Romeo believes: 'Yes, she loved only me'"
- **Score Romeo's f based on his belief about Juliet's faithfulness**

✅ **Correct Thought Process:**
- "Romeo sees Juliet dead"
- "Juliet's presence (even dead) evokes Romeo's relational state"
- "Romeo's faithfulness TO Juliet: Does he remain committed?"
- "Yes - he drinks poison to join her"
- **Score Romeo's f = 9 (his own faithfulness to her)**

### Why The Framework Is Designed This Way

**Tractability:** You can reliably ask subjects "How faithful are you to X?" but not "How faithful do you think X is to you?"

The first is **first-person knowledge** (direct self-report).  
The second is **theory-of-mind inference** (projection, paranoia, idealization).

**Data collection feasibility:**
- ✅ Interview Romeo: "How faithful are you to Juliet?" → Reliable answer
- ❌ Interview Romeo: "How faithful is Juliet to you?" → Romeo's paranoia/idealization, not truth

The framework is **phenomenological** (what M1 experiences) not **cognitive** (what M1 believes about M2).

## The Framework

### M1 File (e.g., Romeo)
M1's gamma_self trajectory - M1's primitives **evoked because of M2 (Juliet)**:

- **v (visibility)**: "I see / I am seen" - M1's visibility in relation to M2
- **r (resonance)**: "I resonate with M2" - M1's resonance with M2
- **f (fidelity)**: "I am faithful to M2" - **M1's faithfulness TO M2**
- **a (agency)**: "I act / I take initiative" - M1's agency in the relationship
- **S (soul presence)**: "I am authentically present" - M1's soul presence with M2

### M2 File (e.g., Juliet)
M2's gamma_self trajectory - M2's primitives **evoked because of M1 (Romeo)**:

- **v (visibility)**: "I see / I am seen" - M2's visibility in relation to M1
- **r (resonance)**: "I resonate with M1" - M2's resonance with M1
- **f (fidelity)**: "I am faithful to M1" - **M2's faithfulness TO M1**
- **a (agency)**: "I act / I take initiative" - M2's agency in the relationship
- **S (soul presence)**: "I am authentically present" - M2's soul presence with M1

## Key Insight: Fidelity Direction

**The most common error:** Scoring M1's perception of M2's faithfulness in M1's file.

❌ **WRONG:**
```
Romeo's file, f=9: "Romeo perceives Juliet as faithful to him"
```

✅ **CORRECT:**
```
Romeo's file, f=9: "Romeo remains faithful to Juliet"
```

Fidelity represents **M1's faithfulness TO M2**, not M1's perception of M2's faithfulness.

## Examples

### Correct Modeling: Romeo & Juliet Tomb Scene

**Romeo's file (M1):**
- f = 9: Romeo remains faithful to Juliet (even believing she's dead)
- v = 10: Romeo sees Juliet fully
- a = 10: Romeo takes decisive action (drinks poison)

**Juliet's file (M2):**
- f = 9: Juliet remains faithful to Romeo (chooses to join him in death)
- v = 10: Juliet sees Romeo fully
- a = 10: Juliet takes decisive action (stabs herself)

### Incorrect Modeling (External Observer Mistake)

❌ **WRONG - External Observer View:**
```
Romeo's file:
- v = 10: "We (observers) see Romeo clearly"
- f = 9: "Romeo perceives Juliet as faithful"
- a = 10: "Romeo is taking lots of action"
```

This confuses perception of M2 with M1's own primitives evoked by M2.

## Common Pitfalls

### 1. Confusing "Who Does What" with "Who Experiences What"
- Primitive values represent **M1's internal state**, not external actions
- Don't ask: "What is M1 doing?"
- Ask: "What is M1 experiencing about M2?"

### 2. Scoring Fidelity Backwards
- M1's file tracks **M1's faithfulness TO M2**
- Not M1's perception of M2's faithfulness to M1
- Fidelity is what M1 **gives**, not what M1 receives

### 3. Mixing Observer and Subject Perspective
- Primitives aren't journalist reporting ("Romeo kissed Juliet")
- They're phenomenological experience ("I feel seen, I perceive her faithfulness")

### 4. Treating M1/M2 as Labels Instead of Perspectives
- M1/M2 aren't "Person A" and "Person B"
- They're **Subject 1's view of Subject 2** and **Subject 2's view of Subject 1**
- Two subjective experiences of the same relationship

## Validation Checklist

Before finalizing any M1 file, ask:
- [ ] Are these M1's own primitives evoked **because of M2**?
- [ ] Does fidelity reflect **M1's faithfulness TO M2**?
- [ ] Am I scoring M1's engagement/presence, not external observations?
- [ ] Would these values represent M1's relational state with M2?

## Edge Cases

### Single-Subject Scenarios
For scenarios with only one person (Buddha, Hachiko waiting):
- M1 = Subject
- M2 = The "other" (enlightenment, absent owner, company, God)
- Still apply subjective framework

### Group Dynamics (Hate Company)
- M1 = Employee
- M2 = Company (collective entity)
- Score employee's subjective experience of company's faithfulness/visibility/etc.

### Asymmetric Awareness
If M1 doesn't know M2's true state:
- Score based on M1's **belief**, not objective truth
- Example: Romeo believes Juliet is dead (f should reflect his perception of her prior faithfulness, not knowledge of her plan)

## Quick Reference Table

| Primitive | M1 File Asks | M2 File Asks |
|-----------|--------------|--------------|
| **v** | Am I visible / do I see in relation to M2? | Am I visible / do I see in relation to M1? |
| **r** | Do I resonate with M2? | Do I resonate with M1? |
| **f** | Am I faithful to M2? | Am I faithful to M1? |
| **a** | Am I acting with agency? | Am I acting with agency? |
| **S** | Am I authentically present? | Am I authentically present? |

## Documentation Best Practice

When creating scenarios, include notes like:
```csv
day,v,r,f,a,S,notes
5,10,10,9,10,10,Tomb – Romeo remains faithful to Juliet (f=9); dies loving her
```

Explicitly state which subject's primitives you're modeling to avoid confusion.

## Summary

**The Golden Rule:** Every primitive in M1's file represents M1's own v, r, f, a, S evoked **because of M2**.

Not "What is M2 doing?" or "What do I perceive about M2?" but "What is my relational state caused by M2?"
