import sys
from prototype import not_implemented

if __name__ == "__main__":
    print("40.230: Phase A only")
    try:
        not_implemented()
    except NotImplementedError:
        sys.exit(2)