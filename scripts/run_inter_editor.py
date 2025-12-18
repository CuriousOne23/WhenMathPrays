import subprocess
import sys

# "data/library/love/single_dating_to_love_M1.csv"
# "data/verification_data/entropy_calibration_M1.csv"


if __name__ == "__main__":
    target_file = "data/library/love/single_dating_to_love_M1.csv"
    print(f"[DEBUG] Attempting to open: {target_file}")

    cmd = [
        sys.executable,
        "tools/interactive_editor.py",
        target_file
    ]
    try:
        # Don't capture output - let it flow directly to terminal for immediate error visibility
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running interactive editor: {e}", file=sys.stderr)
        sys.exit(1)
