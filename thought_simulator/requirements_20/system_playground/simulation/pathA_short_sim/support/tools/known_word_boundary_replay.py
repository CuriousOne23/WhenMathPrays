"""An unknown content word is not invented into a claim."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    unknown = _claim("zyzzyx qwop")
    noun = _claim("The zyzzyx is blue.")
    state = _claim("The sky is zyzzyx.")
    plain = _claim("The sky is blue.")
    print("unknown", repr(unknown))
    print("noun", repr(noun))
    print("state", repr(state))
    print("plain", plain)
    assert unknown == ""
    assert noun == ""
    assert state == ""
    assert plain == "the sky is blue"
    print("known-word boundary replay passed")


if __name__ == "__main__":
    main()
