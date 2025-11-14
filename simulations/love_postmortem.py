# simulations/love_postmortem.py
import numpy as np
import matplotlib.pyplot as plt
from core.love import gamma_self, love
from tqdm import tqdm
import os

def simulate_couple(seed, duration=365):
    np.random.seed(seed)
    t = np.arange(duration)
    
    ego1 = np.random.lognormal(0.4, 0.9, duration)
    bond1to2 = np.random.normal(1.0, 2.0, duration)
    gamma1 = [gamma_self(ego1[i], bond1to2[i]) for i in range(duration)]
    
    ego2 = np.random.lognormal(0.4, 0.9, duration)
    bond2to1 = np.random.normal(1.0, 2.0, duration)
    gamma2 = [gamma_self(ego2[i], bond2to1[i]) for i in range(duration)]
    
    L1, L2 = [], []
    for i in range(duration):
        try:
            L1.append(love(1.0, gamma1[:i+1], t=i))
            L2.append(love(1.0, gamma2[:i+1], t=i))
        except:
            L1.append(0j)
            L2.append(0j)
    
    return {
        'L1': np.array(L1), 'L2': np.array(L2),
        'gamma1': gamma1, 'gamma2': gamma2,
        'ego1': ego1, 'bond1to2': bond1to2,
        'ego2': ego2, 'bond2to1': bond2to1
    }

def classify_couple(data):
    L1, L2 = data['L1'], data['L2']
    last_100 = slice(-100, None)
    
    love_dead = (np.abs(L1[last_100]).mean() < 0.1) and (np.abs(L2[last_100]).mean() < 0.1)
    thriving = (np.abs(L1[last_100]).mean() > 0.2) and (np.abs(L2[last_100]).mean() > 0.2)
    soul_scream = (np.abs(data['gamma1']).max() > 20) or (np.abs(data['gamma2']).max() > 20)
    secure_arc = (L1[-1].real > 0.1 and L1[-1].imag > 0.1 and
                  L2[-1].real > 0.1 and L2[-1].imag > 0.1)
    
    return {
        'love_dead': love_dead,
        'thriving': thriving,
        'soul_scream': soul_scream and love_dead,
        'secure_arc': secure_arc
    }

def extract_features(data):
    L1, L2 = data['L1'], data['L2']
    g1, g2 = data['gamma1'], data['gamma2']
    e1, e2 = data['ego1'], data['ego2']
    b12, b21 = data['bond1to2'], data['bond2to1']
    
    return {
        'final_L': np.mean([np.abs(L1[-1]), np.abs(L2[-1])]),
        'max_gamma': max(np.abs(g1).max(), np.abs(g2).max()),
        'mean_ego': np.mean([e1.mean(), e2.mean()]),
        'mean_bond': np.mean([b12.mean(), b21.mean()]),
        'var_ego': np.mean([e1.var(), e2.var()]),
        'var_bond': np.mean([b12.var(), b21.var()]),
        'sync_bond': np.corrcoef(b12, b21)[0,1],
        'entropy_slope': np.polyfit(np.arange(365), np.log(np.abs(L1) + 1e-10), 1)[0]
    }

# === RUN 100 COUPLES ===
groups = {'love_dead': [], 'thriving': [], 'soul_screamers': [], 'secure_arc': []}
features = []

for seed in tqdm(range(100), desc="Simulating 100 Couples"):
    data = simulate_couple(seed)
    cls = classify_couple(data)
    feat = extract_features(data)
    feat.update(cls)
    features.append(feat)
    
    if cls['love_dead'] and not cls['soul_scream']:
        groups['love_dead'].append(feat)
    if cls['thriving']:
        groups['thriving'].append(feat)
    if cls['soul_scream']:
        groups['soul_screamers'].append(feat)
    if cls['secure_arc']:
        groups['secure_arc'].append(feat)

# === POSTMORTEM REPORT ===
print("\nULep v1.7 — POSTMORTEM: WHY LOVE DIES OR THRIVES")
print("="*60)
for name, group in groups.items():
    if not group: continue
    n = len(group)
    print(f"\n{name.upper().replace('_', ' ')} ({n} couples)")
    print("-"*40)
    print(f"Final |L|:      {np.mean([f['final_L'] for f in group]):.4f}")
    print(f"Max |γ_self|:   {np.mean([f['max_gamma'] for f in group]):.2f}")
    print(f"Mean Ego:       {np.mean([f['mean_ego'] for f in group]):.2f}")
    print(f"Mean Bond:      {np.mean([f['mean_bond'] for f in group]):.2f}")
    print(f"Ego Variance:   {np.mean([f['var_ego'] for f in group]):.2f}")
    print(f"Bond Variance:  {np.mean([f['var_bond'] for f in group]):.2f}")
    print(f"Bond Sync:      {np.mean([f['sync_bond'] for f in group]):.3f}")
    print(f"Entropy Slope:  {np.mean([f['entropy_slope'] for f in group]):.4f}")

# === SAVE PLOT ===
plt.figure(figsize=(12, 8))
for i, (name, group) in enumerate(groups.items()):
    if not group: continue
    x = [f['mean_ego'] for f in group]
    y = [f['mean_bond'] for f in group]
    plt.scatter(x, y, label=f"{name} ({len(group)})", alpha=0.7)
plt.xlabel("Mean Ego Flux")
plt.ylabel("Mean Bond Flux")
plt.title("Why Love Dies or Thrives — 100 Couples")
plt.legend()
plt.grid(True, alpha=0.3)

script_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(script_dir, "love_postmortem.png"), dpi=150, bbox_inches='tight')
print(f"\nPlot saved: love_postmortem.png")