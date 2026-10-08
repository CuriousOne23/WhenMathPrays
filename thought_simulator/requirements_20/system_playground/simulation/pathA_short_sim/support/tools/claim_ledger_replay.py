"""The claim ledger matches the runner. An unknown string stays empty."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


ROWS = [
    ("The sky is blue.", "the sky is blue"),
    ("The book is on the table.", "the book is on the table"),
    ("The cat chased the mouse.", "the cat chased the mouse"),
    ("The quick brown fox jumps over the lazy dog.", "the quick brown fox jumps over the lazy dog"),
    ("The rain in Spain stays mainly in the plain.", "the rain stays mainly in spain in the plain"),
    ("Where is the book?", "where is the book"),
    ("Why is the sky blue?", "why is the sky blue"),
    ("Is the book on the table?", "is the book on the table"),
    ("Close the door.", "close the door"),
    ("Please close the door.", "please close the door"),
    ("Give me the book.", "give me the book"),
    ("She said the book is on the table.", "she said the book is on the table"),
    ("The book that John bought.", "the book that john bought"),
    ("What a beautiful lamp!", "exclamative a beautiful lamp"),
    ("LLhfds pw Ppen qqoubx&", ""),
]


def main() -> None:
    for raw, expected in ROWS:
        tp = run_pathA_short(raw)["final_tp"]
        claim = claim_from_packet(tp)["claim"]
        print(raw, claim)
        assert claim == expected, (raw, claim, expected)
        assert list(tp.get("struct_segments") or []) == list(tp.get("struct_segments") or [])
    print("claim-ledger replay passed")


if __name__ == "__main__":
    main()
