"""A selected op off the relation list is a hole, not a new relation."""

from idob.connections import connections_from_packet
from pathA_short_simulator import run_pathA_short


def main() -> None:
    polar = connections_from_packet(run_pathA_short("Is the book on the table?")["final_tp"])
    plain = connections_from_packet(run_pathA_short("The sky is blue.")["final_tp"])
    print("polar", polar["holes"], polar["notices"])
    print("plain", plain["notices"])
    assert any(item["relation"] == "polar_question" and item["status"] == "missing" for item in polar["holes"])
    assert "unlisted_op" in polar["notices"]
    assert "unlisted_op" not in plain["notices"]
    assert all(item["relation"] != "polar_question" for item in polar["connections"])
    print("s2m-unlisted-op replay passed")


if __name__ == "__main__":
    main()
