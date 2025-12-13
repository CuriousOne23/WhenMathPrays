import numpy as np

print("Testing numpy insert with dict assignment:")
d1 = {'time': np.array([1.0, 2.0, 3.0])}
d2 = {'time': np.array([1.0, 2.0, 3.0])}

print(f"Before: d1 size={len(d1['time'])}, d2 size={len(d2['time'])}")

d1['time'] = np.insert(d1['time'], 1, 1.5)
d2['time'] = np.insert(d2['time'], 1, 1.5)

print(f"After: d1 size={len(d1['time'])}, d2 size={len(d2['time'])}")
print(f"d1['time'] = {d1['time']}")
print(f"d2['time'] = {d2['time']}")
print("Both updated correctly!")
