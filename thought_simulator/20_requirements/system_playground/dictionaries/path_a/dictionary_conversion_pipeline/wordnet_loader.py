import os
from pathlib import Path

class WordNetSynset:
    """
    Represents a single WordNet synset loaded from data.* files.
    """
    def __init__(self, offset, pos, lemma_list, gloss, pointers):
        self.offset = offset          # integer offset in data file
        self.pos = pos                # noun, verb, adj, adv
        self.lemmas = lemma_list      # list of lemmas
        self.gloss = gloss            # raw gloss text
        self.pointers = pointers      # semantic relations

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

        self.index = {}   # lemma → list of synset offsets
        self.synsets = {} # offset → WordNetSynset

    def load(self):
        self._load_index_files()
        self._load_data_files()
        return self.index, self.synsets

    # ------------------------------------------------------------
    # INDEX FILE PARSER
    # ------------------------------------------------------------
    def _load_index_files(self):
        for pos, file_path in self.index_files.items():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("  ") or line.startswith(" "):
                        continue
                    if line.startswith("synset"):
                        continue
                    if line.startswith("lemma"):
                        continue
                    if line.startswith("  "):
                        continue
                    if line.strip() == "":
                        continue
                    if line.startswith("#"):
                        continue

                    parts = line.strip().split()
                    lemma = parts[0]
                    synset_count = int(parts[3])
                    offsets = parts[-synset_count:]

                    self.index.setdefault(lemma, [])
                    self.index[lemma].extend([(pos, int(o)) for o in offsets])

    # ------------------------------------------------------------
    # DATA FILE PARSER
    # ------------------------------------------------------------
    def _load_data_files(self):
        for pos, file_path in self.data_files.items():
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("  ") or line.startswith(" "):
                        continue
                    if line.strip() == "":
                        continue
                    if line.startswith("#"):
                        continue

                    parts = line.strip().split(" | ")
                    data_part = parts[0]
                    gloss = parts[1] if len(parts) > 1 else ""

                    fields = data_part.split()
                    offset = int(fields[0])
                    lemma_count = int(fields[3])
                    lemma_list = fields[4:4 + lemma_count]

                    pointer_count_index = 4 + lemma_count
                    pointer_count = int(fields[pointer_count_index])
                    pointer_start = pointer_count_index + 1
                    pointer_end = pointer_start + pointer_count

                    pointers = fields[pointer_start:pointer_end]

                    synset = WordNetSynset(
                        offset=offset,
                        pos=pos,
                        lemma_list=lemma_list,
                        gloss=gloss,
                        pointers=pointers
                    )

                    self.synsets[(pos, offset)] = synset

# ------------------------------------------------------------
# Convenience function
# ------------------------------------------------------------
def load_wordnet(base_dir="wordnet_raw"):
    loader = WordNetLoader(base_dir)
    return loader.load()
