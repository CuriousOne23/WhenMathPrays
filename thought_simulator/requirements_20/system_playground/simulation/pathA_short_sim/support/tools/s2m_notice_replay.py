"""Two supported relations are noticed and not ranked."""

from idob.connections import connections_from_packet
from pathA_short_simulator import run_pathA_short


def main() -> None:
    plain = connections_from_packet(run_pathA_short("The sky is blue.")["final_tp"])
    unknown = connections_from_packet(run_pathA_short("LLhfds pw Ppen qqoubx&")["final_tp"])
    print("plain", plain["notices"], len(plain["connections"]))
    print("unknown", unknown["notices"])
    assert plain["notices"] == ["underspecified"]
    assert len(plain["connections"]) >= 2
    assert unknown["notices"] == []
    assert all("likelihood" not in item for item in plain["connections"])
    print("s2m-notice replay passed")


if __name__ == "__main__":
    main()
