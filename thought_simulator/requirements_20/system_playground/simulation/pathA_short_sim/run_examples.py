from pathA_short_simulator import run_pathA_short


def main() -> None:
    sentence = "The quick brown fox jumps over the lazy dog."
    result = run_pathA_short(sentence)

    print("=== Final TP ===")
    for k, v in result["final_tp"].items():
        print(f"{k}: {v}")

    print("\n=== Trace ===")
    for step in result["trace"]:
        print(f"\n--- {step['primitive']} ---")
        print(f"notes: {step['notes']}")
        # If you want more detail, uncomment:
        # print("input:", step["input"])
        # print("output:", step["output"])


if __name__ == "__main__":
    main()

