def test_debug_example():
    x = 42
    y = x * 2
    z = y + 5
    print(f"x={x}, y={y}, z={z}")
    # Place a breakpoint on the next line to inspect variables
    return z

if __name__ == "__main__":
    result = test_debug_example()
    print(f"Result: {result}")
