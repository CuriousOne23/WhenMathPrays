"""A command claims its theme when the packet has one."""

from idob.claim import claim_from_packet
from pathA_short_simulator import run_pathA_short


def _claim(raw: str) -> str:
    return claim_from_packet(run_pathA_short(raw)["final_tp"])["claim"]


def main() -> None:
    command = _claim("Close the door.")
    please = _claim("Please close the door.")
    plain = _claim("The sky is blue.")
    print("command", command)
    print("please", please)
    print("plain", plain)
    assert command == "close the door", command
    assert please == "please close the door", please
    assert plain == "the sky is blue"
    print("command-theme claim replay passed")


if __name__ == "__main__":
    main()
