# ⭐ **SOB Field Set (Final, Architecturally Correct)**  
SOB captures **only structure**, never meaning.  
Fields are grouped by structural domain.

---

## 🟦 **1. Message‑Level Structural Form**
These describe the *global shape* of the message.

- **sob_sentence_count** — bounded count (0–15)  
- **sob_clause_count** — commas, semicolons, conjunction boundaries  
- **sob_interrogative_flag** — ends with “?”  
- **sob_imperative_flag** — verb‑initial pattern  
- **sob_declarative_flag** — ends with “.”  
- **sob_exclamatory_flag** — ends with “!”  
- **sob_fragment_flag** — no terminal punctuation  

These are purely structural, no semantics.

---

## 🟦 **2. Tokenization & Layout Structure**
These describe how the message is physically arranged.

- **sob_token_count** — bounded token count  
- **sob_avg_token_length** — quantized  
- **sob_max_token_length** — quantized  
- **sob_line_count** — newline‑separated lines  
- **sob_paragraph_count** — blank‑line‑separated blocks  
- **sob_list_flag** — “-”, “*”, “1.” at line start  
- **sob_code_block_flag** — triple backticks or indentation pattern  
- **sob_json_like_flag** — braces + colon pattern  
- **sob_table_like_flag** — pipe‑delimited or grid pattern  

These fields tell RB the **layout mode**.

---

## 🟦 **3. Punctuation & Symbol Pattern**
These are the most important for routing because they produce stable bitmasks.

- **sob_punctuation_mask** — bitmask for:  
  comma, semicolon, colon, dash, parentheses, brackets, braces, quotes, ellipsis, slash, backslash  
- **sob_punctuation_density** — quantized ratio  
- **sob_capitalization_mask** — ALLCAPS, TitleCase, camelCase, mixed  
- **sob_digit_flag** — digits present  
- **sob_symbol_flag** — %, $, @, #, &, etc.  

These are **non-semantic structural cues**.

---

## 🟦 **4. Boundary & Delimiter Structure**
These describe how the message is segmented.

- **sob_boundary_mask** — sentence, clause, parenthetical, quote boundaries  
- **sob_indent_pattern** — none / uniform / mixed / code‑like  
- **sob_whitespace_pattern** — tabs, multiple spaces, leading/trailing  
- **sob_markup_flag** — HTML‑like / Markdown‑like / LaTeX‑like  
- **sob_inline_code_flag** — backtick‑delimited spans  

These help RB detect **structural modes**.

---

## 🟦 **5. Structural Rhythm & Distribution**
These fields capture “shape over time” without meaning.

- **sob_token_length_histogram** — coarse 4‑bin histogram  
- **sob_sentence_length_histogram** — coarse 4‑bin histogram  
- **sob_clause_length_histogram** — coarse 4‑bin histogram  
- **sob_symbol_run_pattern** — repeated symbols, e.g., “---”, “===”  

These are extremely stable under noise.

---

## 🟦 **6. SOB Output Packaging**
SOB outputs:

```
sob_residue = {
    sob_fields: [...],      # bounded list of normalized structural fields
    sob_bitmask: <uintN>,   # compressed structural mask
    sob_checksum: <uint64>, # integrity check
}
