"""Joined claims keep action, state, and query without doubling."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    fox = _claim("The quick brown fox jumps over the lazy dog.")
    rain = _claim("The rain in Spain stays mainly in the plain.")
    why = _claim("Why is the sky blue?")
    plain = _claim("The sky is blue.")
    print("fox", fox)
    print("rain", rain)
    print("why", why)
    print("plain", plain)
    assert fox == "the quick brown fox jumps over the lazy dog", fox
    assert rain == "the rain stays mainly in spain in the plain", rain
    assert why == "why is the sky blue", why
    assert plain == "the sky is blue"
    print("claim-join replay passed")


if __name__ == "__main__":
    main()
