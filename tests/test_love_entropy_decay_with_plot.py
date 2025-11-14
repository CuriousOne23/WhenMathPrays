# tests/test_love_entropy_decay_with_plot.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from core.love import gamma_self, love


def test_love_entropy_decay_with_plot():
    """
    Test entropy decay with NOISE and 6 plots:
      1. |L(t)| vs time
      2. Re(L), Im(L) vs time
      3. L(t) in complex plane
      4. γ_self in complex plane
      5. Entropy factor: exp(-ΔS t)
      6. Noise realization (real + imag)
    ALL PLOTS SAVED TO tests/
    """
    W = 1.0
    delta_S = 0.1
    tw = 0
    days = 10
    times = np.arange(days + 1)
    noise = 0.05

    g_fixed = gamma_self(we_ego_state=1.0, love_enmity_state=0.0)

    L_t = []
    gamma_t = []
    entropy_factor = []
    noise_real = []
    noise_imag = []
    for t in times:
        L = love(W=W, gamma_history=[g_fixed], tw=tw, t=t, delta_S=delta_S, noise=noise)
        L_t.append(L)
        gamma_t.append(g_fixed)
        entropy_factor.append(np.exp(-delta_S * t))
        noise_real.append(L.real - (np.exp(1.0 - delta_S * t)))
        noise_imag.append(L.imag)

    L_t = np.array(L_t)
    gamma_t = np.array(gamma_t)
    entropy_factor = np.array(entropy_factor)
    noise_real = np.array(noise_real)
    noise_imag = np.array(noise_imag)

    # === OUTPUT DIRECTORY: tests/ ===
    output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)

    # === PLOT 1: |L(t)| vs time ===
    plt.figure(figsize=(10, 6))
    plt.plot(times, np.abs(L_t), 'o-', color='purple', label='|L(t)|')
    plt.plot(times, np.exp(1.0 - delta_S * times), '--', color='green', label='|L(t)| without noise')
    plt.xlabel("Time (days)")
    plt.ylabel("|L(t)| — Love Intensity")
    plt.title("Entropy Decay with Noise")
    plt.legend()
    plt.grid(True, alpha=0.3)
    for i, t_val in enumerate(times):
        plt.annotate(f"t={i}", (t_val, np.abs(L_t[i])), xytext=(5, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_magnitude.png"), dpi=150)
    plt.close()

    # === PLOT 2: Re(L), Im(L) vs time ===
    plt.figure(figsize=(10, 6))
    plt.plot(times, L_t.real, 's-', color='blue', label='Re(L(t))')
    plt.plot(times, L_t.imag, 'd-', color='red', label='Im(L(t))')
    plt.plot(times, np.exp(1.0 - delta_S * times), '--', color='gray', label='exp(1 - ΔS t)')
    plt.xlabel("Time (days)")
    plt.ylabel("L(t) Components")
    plt.title("Re(L) and Im(L) Over Time with Noise")
    plt.legend()
    plt.grid(True, alpha=0.3)
    for i, t_val in enumerate(times):
        plt.annotate(f"t={i}", (t_val, L_t.real[i]), xytext=(5, 5), textcoords='offset points', color='blue')
        plt.annotate(f"t={i}", (t_val, L_t.imag[i]), xytext=(5, -10), textcoords='offset points', color='red')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_re_im.png"), dpi=150)
    plt.close()

    # === PLOT 3: L(t) in complex plane ===
    plt.figure(figsize=(8, 8))
    plt.scatter(L_t.real, L_t.imag, c='magenta', s=80, zorder=5)
    for i, (re, im) in enumerate(zip(L_t.real, L_t.imag)):
        plt.annotate(f"t={i}", (re, im), xytext=(8, 8), textcoords='offset points', fontsize=9)
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.xlabel("Re(L) — Growth")
    plt.ylabel("Im(L) — Direction")
    plt.title("L(t) Trajectory in Complex Plane with Noise")
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    margin = 0.2
    plt.xlim(min(L_t.real) - margin, max(L_t.real) + margin)
    plt.ylim(min(L_t.imag) - margin, max(L_t.imag) + margin)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_complex_plane.png"), dpi=150)
    plt.close()

    # === PLOT 4: γ_self in complex plane ===
    plt.figure(figsize=(8, 8))
    plt.scatter(gamma_t.real, gamma_t.imag, c='red', s=100, zorder=5)
    for i, (re, im) in enumerate(zip(gamma_t.real, gamma_t.imag)):
        plt.annotate(f"t={i}", (re, im), xytext=(10, 10), textcoords='offset points', fontsize=10)
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.xlabel("Re(γ) — We (+) | I (–)")
    plt.ylabel("Im(γ) — Love (+) | Enmity (–)")
    plt.title("γ_self States (Fixed: +1 + 0j)")
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.xlim(0.5, 1.5)
    plt.ylim(-0.5, 0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_gamma_self.png"), dpi=150)
    plt.close()

    # === PLOT 5: ENTROPY DECAY FACTOR ===
    plt.figure(figsize=(10, 6))
    plt.plot(times, entropy_factor, 'o-', color='darkorange', label='exp(-ΔS t)')
    plt.axhline(1.0, color='gray', linestyle='--', label='t=0')
    plt.xlabel("Time (days)")
    plt.ylabel("Entropy Factor")
    plt.title(f"Entropy Decay: exp(-{delta_S} t)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    for i, t_val in enumerate(times):
        plt.annotate(f"t={i}", (t_val, entropy_factor[i]), xytext=(5, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_entropy_factor.png"), dpi=150)
    plt.close()

    # === PLOT 6: NOISE REALIZATION ===
    plt.figure(figsize=(10, 6))
    plt.plot(times, noise_real, 'o-', color='cyan', label='Noise Real')
    plt.plot(times, noise_imag, 's-', color='magenta', label='Noise Imag')
    plt.axhline(0, color='k', linestyle='-', linewidth=0.5)
    plt.xlabel("Time (days)")
    plt.ylabel("Noise")
    plt.title("Noise in L(t) — Real and Imag")
    plt.legend()
    plt.grid(True, alpha=0.3)
    for i, t_val in enumerate(times):
        plt.annotate(f"t={i}", (t_val, noise_real[i]), xytext=(5, 5), textcoords='offset points', color='cyan')
        plt.annotate(f"t={i}", (t_val, noise_imag[i]), xytext=(5, -10), textcoords='offset points', color='magenta')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "love_entropy_decay_noise.png"), dpi=150)
    plt.close()

    # === ASSERTION ===
    assert abs(L_t[-1]) < abs(L_t[0]) * 0.7
    print("All 6 plots saved to 'tests/' directory. Test PASSED.")


if __name__ == "__main__":
    test_love_entropy_decay_with_plot()