import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "tools/interactive_editor.py",
        "data/library/love/single_dating_to_love_M1.csv"
    ]
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running interactive editor: {e}", file=sys.stderr)
        sys.exit(1)
