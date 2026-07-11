from pathlib import Path

class WordNetSynset:
    """
    Represents a single WordNet synset loaded from data.* files.
    """
    def __init__(self, offset, pos, lex_filenum, lemmas, lex_ids,
                 pointers, gloss):
        self.offset = offset
        self.pos = pos
        self.lex_filenum = lex_filenum
        self.lemmas = lemmas
        self.lex_ids = lex_ids
        self.pointers = pointers
        self.gloss = gloss

    def __repr__(self):
        return f"<Synset {self.pos}:{self.offset} {self.lemmas}>"


class WordNetLoader:
    """
    Loads raw WordNet index.* and data.* files directly.
    Produces synset objects for downstream TS dictionary conversion.
    """

    def __init__(self, base_dir="wordnet_raw"):
        self.base_dir = Path(base_dir)

        self.index_files = {
            "noun": self.base_dir / "index.noun",
            "verb": self.base_dir / "index.verb",
            "adj":  self.base_dir / "index.adj",
            "adv":  self.base_dir / "index.adv",
        }

        self.data_files = {
            "noun": self.base_dir / "data.noun",
            "verb": self.base_dir / "data.verb",
            "adj":  self.base_dir / "data.adj",
            "adv":  self.base_dir / "data.adv",
        }

        self.index = {}   # lemma → list of (pos, offset)
        self.synsets = {} # (pos, offset) → WordNetSynset

    def load(self):
        self._load_index_files()
        self._load_data_files()
        return self.index, self.synsets

    # ------------------------------------------------------------
    # INDEX FILE PARSER
    # ------------------------------------------------------------
    def _load_index_files(self):
        """
        Correct WordNet index.* format:
            lemma  pos  synset_cnt  p_cnt  ptr...  sense_cnt  tagsense_cnt  offsets...
        """
        for pos, file_path in self.index_files.items():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()

                    # Skip malformed or header lines
                    if len(parts) < 6:
                        continue

                    lemma = parts[0]
                    pos_code = parts[1]

                    # synset_cnt and p_cnt must be integers
                    if not parts[2].isdigit() or not parts[3].isdigit():
                        continue

                    synset_cnt = int(parts[2])
                    p_cnt = int(parts[3])

                    # Pointer symbols start at index 4
                    ptr_start = 4
                    ptr_end = ptr_start + p_cnt

                    # After pointer symbols:
                    #   sense_cnt, tagsense_cnt, then offsets
                    if not parts[ptr_end].isdigit() or not parts[ptr_end + 1].isdigit():
                        continue

                    sense_cnt = int(parts[ptr_end])
                    tagsense_cnt = int(parts[ptr_end + 1])

                    offset_start = ptr_end + 2
                    offset_end = offset_start + sense_cnt

                    offsets = parts[offset_start:offset_end]

                    self.index.setdefault(lemma, [])
                    for o in offsets:
                        self.index[lemma].append((pos, int(o)))

    # ------------------------------------------------------------
    # DATA FILE PARSER
    # ------------------------------------------------------------
    def _load_data_files(self):
        """
        data.* format:
            offset lex_filenum pos lemma_cnt lemma lex_id ... ptr_cnt ptr... | gloss
        """
        for pos, file_path in self.data_files.items():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Skip ALL header lines:
                    # WordNet data files begin with many lines like:
                    # "This software and database is being provided..."
                    # "WordNet 3.0 Copyright..."
                    # These must be skipped.
                    if not line[0].isdigit():
                        continue

                    # Split gloss
                    if " | " in line:
                        data_part, gloss = line.split(" | ", 1)
                    else:
                        data_part, gloss = line, ""

                    fields = data_part.split()

                    offset = int(fields[0])
                    lex_filenum = int(fields[1])
                    pos_code = fields[2]

                    lemma_count = int(fields[3])
                    lemma_start = 4
                    lemma_end = lemma_start + lemma_count

                    lemmas = fields[lemma_start:lemma_end]
                    lex_ids = [int(x) for x in fields[lemma_end:lemma_end + lemma_count]]

                    ptr_count_index = lemma_end + lemma_count
                    ptr_count = int(fields[ptr_count_index])

                    ptr_start = ptr_count_index + 1
                    ptr_end = ptr_start + ptr_count * 4

                    pointers_raw = fields[ptr_start:ptr_end]
                    pointers = []
                    for i in range(0, len(pointers_raw), 4):
                        pointers.append({
                            "symbol": pointers_raw[i],
                            "offset": int(pointers_raw[i+1]),
                            "pos": pointers_raw[i+2],
                            "src_tgt": pointers_raw[i+3],
                        })

                    synset = WordNetSynset(
                        offset=offset,
                        pos=pos,
                        lex_filenum=lex_filenum,
                        lemmas=lemmas,
                        lex_ids=lex_ids,
                        pointers=pointers,
                        gloss=gloss,
                    )

                    self.synsets[(pos, offset)] = synset

def load_wordnet(base_dir="wordnet_raw"):
    loader = WordNetLoader(base_dir)
    return loader.load()
