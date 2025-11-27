import numpy as np

STEPS_PER_DAY = 24
DAYS = 60
T = STEPS_PER_DAY * DAYS
DT = 1.0 / STEPS_PER_DAY

def sigmoid(z): return 1.0 / (1.0 + np.exp(-z))

def evolve_gamma(cfg):
    rng = np.random.default_rng(cfg['seed'])
    x, y = cfg['x0'], cfg['y0']
    xi_x, xi_y = 0.0, 0.0
    out = []

    for t in range(T):
        # Progress ramp (turns up attraction/drift mid-suite)
        s = sigmoid(cfg['lambda'] * (t / T - cfg['ramp_center']))

        # AR(1) noise
        xi_x = cfg['rho'] * xi_x + rng.normal()
        xi_y = cfg['rho'] * xi_y + rng.normal()
        eta_x = cfg['sigma'] * xi_x
        eta_y = cfg['sigma'] * xi_y

        # Rotation
        rot_x = -cfg['omega'] * y
        rot_y =  cfg['omega'] * x

        # Soft saturation
        fx = cfg['alpha'] * (x - cfg['beta'] * x**3)
        fy = cfg['alpha'] * (y - cfg['beta'] * y**3)

        # Time-varying drift toward Q1
        dx = cfg['d0'][0] + cfg['d1'][0] * s
        dy = cfg['d0'][1] + cfg['d1'][1] * s

        # Q1 attractor
        ax = cfg['kappa'] * (cfg['cQ1'][0] - x)
        ay = cfg['kappa'] * (cfg['cQ1'][1] - y)

        # Breath impulse
        breath_step = cfg['breath_days'] * STEPS_PER_DAY
        impulse = 1 if (t > 0 and (t % breath_step == 0)) else 0
        bx = impulse * cfg['A_b'] * np.cos(cfg['phi'])
        by = impulse * cfg['A_b'] * np.sin(cfg['phi'])

        # Update (no averaging in gamma_self)
        x += DT * (rot_x + dx + fx + eta_x + ax) + bx
        y += DT * (rot_y + dy + fy + eta_y + ay) + by

        out.append((t, x, y))
    return np.array(out)

def love_from_gamma(gamma, tau_days, gate_fn):
    tau = tau_days * STEPS_PER_DAY
    L = []
    for t in range(len(gamma)):
        start = max(0, t - tau + 1)
        avg = gamma[start:t+1, 1:3].mean(axis=0)
        W = gate_fn(t)
        Lx, Ly = avg * W
        L.append((t, Lx, Ly, np.linalg.norm([Lx, Ly]), W))
    return np.array(L)

# Configs (Q4 -> Q1 for M1; Q3 -> Q1 for M2)
cfg_M1 = {
    'seed': 42, 'x0': +0.45, 'y0': -0.35,
    'omega': +0.006, 'alpha': 0.08, 'beta': 0.90,
    'sigma': 0.015, 'rho': 0.60,
    'd0': [ +0.002, +0.006 ], 'd1': [ +0.003, +0.006 ],
    'kappa': 0.015, 'cQ1': [ +0.35, +0.30 ],
    'breath_days': 10, 'A_b': 0.02, 'phi': np.pi/6,
    'lambda': 8.0, 'ramp_center': 0.40,
}

cfg_M2 = {
    'seed': 99, 'x0': -0.40, 'y0': -0.30,
    'omega': -0.012, 'alpha': 0.10, 'beta': 0.85,
    'sigma': 0.018, 'rho': 0.50,
    'd0': [ +0.006, +0.004 ], 'd1': [ +0.006, +0.004 ],
    'kappa': 0.018, 'cQ1': [ +0.35, +0.30 ],
    'breath_days': 10, 'A_b': 0.02, 'phi': -np.pi/8,
    'lambda': 8.0, 'ramp_center': 0.40,
}

def gate_W(t):
    # Gentle openness ramp into Q1 without distorting direction
    s = sigmoid(8.0 * (t / T - 0.40))
    return 1.0 + 0.2 * s  # in [1.0, 1.2]

gamma_M1 = evolve_gamma(cfg_M1)
gamma_M2 = evolve_gamma(cfg_M2)

love_M1 = love_from_gamma(gamma_M1, tau_days=10, gate_fn=gate_W)
love_M2 = love_from_gamma(gamma_M2, tau_days=10, gate_fn=gate_W)
