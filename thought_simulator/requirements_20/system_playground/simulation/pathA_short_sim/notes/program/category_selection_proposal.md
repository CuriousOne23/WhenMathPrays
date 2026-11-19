# Category selection proposal

**Document:** notes/program/category_selection_proposal.md  
**Status:** Draft / discussion  
**Date:** 2026-11-19  
**Points from:** short-sim status (prior S2M seed goal is now historical)

## Why this is next

The narrow S2M seed (accountability trail + interpretive transfer) is now attached by IdOB and visible. The next controlled step is to let a category be chosen instead of always taking the default. Two distinct sources of information can drive that choice. Both stay recoverable and do not mutate the floor.

## Two realization paths

### 1. Sentence-internal modification (information is in the sentence)

- The utterance itself carries a cue that selects a non-default category.
- Example shape: a modifier, an adverb, or a structural marker already written by the floor (SOB/SROB/CnOB/SmOB) is read as a category cue.
- IdOB reads the cue, proposes the category, and records the choice in the seed/meaning packet.
- No prior context is required. The default remains the floor path when the cue is absent.

### 2. CEx from prior CIL (prior conversation supplies the information)

- A prior utterance (held in CIL) contains the cue.
- The present utterance is compared against that prior utterance via CEx.
- When the comparison shows the prior utterance licenses a different category, CEx writes a category-selection packet.
- IdOB reads that packet (or the CEx result) and chooses the non-default category.
- The present utterance itself may contain no explicit cue; the history supplies it.
- Default remains active when no prior cue is present or when the comparison fails.

## Shared constraints

- Category choice is additive and optional (CLI or flag controlled, same pattern as the current seed).
- Floor writers (SOB–SmOB) are not mutated.
- Crossing fields stay null until a later, explicit stage writes them.
- Both paths produce a readable record: which category was chosen, why (sentence cue vs prior-CEx cue), and what the default would have been.
- Requirements remain unchanged until the realization is shown to be legitimate.

## Expected visible output (sketch)

```
--- Category selection (IdOB) ---
chosen_category: ...
source: sentence | prior_cex
default_category: ...
cue: ...
```

## Relation to prior work

This proposal follows the successfully realized narrow S2M seed (accountability trail + interpretive transfer). That prior goal is now historical and recorded as accomplished in the short-sim status page.
