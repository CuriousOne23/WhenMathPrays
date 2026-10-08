"""A reporting op with a speaker is a connection. No speaker is a hole."""

from idob.connections import connections_from_packet
from pathA_short_simulator import run_pathA_short


def main() -> None:
    said = connections_from_packet(run_pathA_short("She said the book is on the table.")["final_tp"])
    plain = connections_from_packet(run_pathA_short("The book is on the table.")["final_tp"])
    print("said", [item["relation"] for item in said["connections"]])
    print("plain", [item["relation"] for item in plain["connections"]])
    assert any(item["relation"] == "reporting" and item["left"] == "she" for item in said["connections"])
    assert all(item["relation"] != "reporting" for item in plain["connections"])
    print("s2m-reporting-link replay passed")


if __name__ == "__main__":
    main()
