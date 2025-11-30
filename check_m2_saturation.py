import pandas as pd

df = pd.read_csv('data/Test2_Parent_Child/Test2_Parent_Child_M2_gamma_self_table.csv', sep='\t', skiprows=2)

# Convert to computer scale
v_comp = df['Visibility v(t)'] / 20 + 0.5
r_comp = df['Resonance r(t)'] / 20 + 0.5
f_comp = df['Fidelity f(t)'] / 20 + 0.5
a_comp = df['Alturism a(t)'] / 20 + 0.5

# Check saturation at each event
for idx, row in df.iterrows():
    v = v_comp.iloc[idx]
    r = r_comp.iloc[idx]
    f = f_comp.iloc[idx]
    a = a_comp.iloc[idx]
    
    count_83 = sum([v >= 0.83, r >= 0.83, f >= 0.83, a >= 0.83])
    count_80 = sum([v >= 0.80, r >= 0.80, f >= 0.80, a >= 0.80])
    
    if count_83 >= 3 or count_80 >= 4:
        print(f"Day {row['Day']:.0f}: v={v:.3f}, r={r:.3f}, f={f:.3f}, a={a:.3f} | ≥0.83: {count_83}, ≥0.80: {count_80}")
