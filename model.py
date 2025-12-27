import numpy as np
import matplotlib.pyplot as plt

def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    if n < 1e-9:
        return v
    return v / n

def transverse_noise(d, sigma):
    r = np.random.randn(3)
    r -= np.dot(r, d) * d
    return unit(d + sigma * r)

def grow_trunk(start, direction, steps, step=1.6, sigma=0.02):
    pts = [start.copy()]
    pos = start.copy()
    d = unit(direction)

    for _ in range(steps):
        d = transverse_noise(d, sigma)
        pos = pos + step * d
        pts.append(pos.copy())

    return np.array(pts)

def grow_branch(start, direction, steps,
                step=1.2,
                angle_std=0.22,
                branch_prob=0.06):
    pts = [start.copy()]
    pos = start.copy()
    d = unit(direction)
    seeds = []

    for _ in range(steps):
        d = unit(d + angle_std * np.random.randn(3))
        pos = pos + step * d
        pts.append(pos.copy())

        if np.random.rand() < branch_prob:
            seeds.append((pos.copy(),
                          unit(d + 0.4 * np.random.randn(3)),
                          int(steps * 0.55)))

    return np.array(pts), seeds

def recursive_branch(start, direction, steps, depth):
    if depth == 0 or steps < 5:
        return []

    segs = []
    pts, seeds = grow_branch(
        start,
        direction,
        steps=steps,
        branch_prob=0.07,
        angle_std=0.24
    )
    segs.append(pts)

    for s in seeds[:2]:
        segs += recursive_branch(
            s[0],
            unit(s[1] + 0.25 * np.random.randn(3)),
            s[2],
            depth - 1
        )

    return segs

def pyramidal_neuron(origin):
    segs = []

    # apical trunk
    trunk = grow_trunk(
        origin,
        direction=[0, 1, 0],
        steps=140
    )
    segs.append(trunk)

    # apical tuft (dense, recursive)
    for p in trunk[-90::10]:
        segs += recursive_branch(
            p,
            unit([0, 1, 0] + 0.15 * np.random.randn(3)),
            steps=50,
            depth=3
        )

    # basal dendrites
    for _ in range(5):
        segs += recursive_branch(
            origin,
            unit([np.random.randn(), -0.4, np.random.randn()]),
            steps=70,
            depth=3
        )

    return segs

def single_neuron():
    segs = []
    origin = np.zeros(3)

    for _ in range(10):
        segs += recursive_branch(
            origin,
            unit(np.random.randn(3)),
            steps=90,
            depth=3
        )

    return segs

def cable_bundle():
    bundle = []
    somas = []

    n_cables = 7
    y_positions = np.linspace(140, 320, n_cables)

    for i, y in enumerate(y_positions):
        soma = np.array([180, y, 200])
        somas.append(soma)

        direction = unit([
            1.0,
            0.15 * np.random.randn(),   # rozrzut boczny
            -0.25 + 0.1*np.random.randn()
        ])

        cable = grow_trunk(
            start=soma,
            direction=direction,
            steps=95,
            step=1.7,
            sigma=0.01
        )

        bundle.append(cable)

    return bundle, somas

def pruning_neuron():
    segs = []
    origin = np.array([260, 260, 260])

    for _ in range(6):
        segs += recursive_branch(
            origin,
            unit(np.random.randn(3)),
            steps=70,
            depth=3
        )

    return origin, segs


def prune(segs, keep_fraction=0.4):
    n = int(len(segs) * keep_fraction)
    return segs[:n]

np.random.seed(4)

fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.0])

axA = fig.add_subplot(gs[0, :])
axB = fig.add_subplot(gs[1, 0])
axC1 = fig.add_subplot(gs[1, 1], projection="3d")
axC2 = fig.add_subplot(gs[1, 1], projection="3d")
axD1 = fig.add_subplot(gs[1, 2], projection="3d")
axD2 = fig.add_subplot(gs[1, 2], projection="3d")

xs = np.linspace(40, 520, 8)
for x in xs:
    origin = np.array([x, 40, 0])
    for s in pyramidal_neuron(origin):
        axA.plot(s[:, 0], s[:, 1], lw=0.9)

axA.scatter(xs, [40]*len(xs), s=30)
axA.axis("off")
axA.text(0.01, 0.96, "A", transform=axA.transAxes,
         fontsize=16, fontweight="bold")

for s in single_neuron():
    axB.plot(s[:, 0], s[:, 2], color="red", lw=0.9)

axB.scatter([0], [0], s=80, color="red")
axB.set_aspect("equal")
axB.axis("off")
axB.text(-0.08, 1.05, "B", transform=axB.transAxes,
         fontsize=16, fontweight="bold")

bundle, somas = cable_bundle()

for ax in [axC1, axC2]:
    for cable in bundle:
        ax.plot(cable[:, 0], cable[:, 1], cable[:, 2], lw=3)

        # ŚRODEK kabla
        mid_idx = len(cable) // 2
        mid_pt = cable[mid_idx]

        ax.scatter(
            [mid_pt[0]],
            [mid_pt[1]],
            [mid_pt[2]],
            s=160,
            c="gray"
        )

    ax.scatter([250], [100], [80], c="red", marker="+", s=70)

    ax.set_xlim(80, 380)
    ax.set_ylim(100, 360)
    ax.set_zlim(80, 360)

axC1.view_init(25, -55)
axC2.view_init(25, -35)

axC1.text2D(
    -0.15, 1.05, "C",
    transform=axC1.transAxes,
    fontsize=16,
    fontweight="bold"
)

soma, full = pruning_neuron()
pruned = prune(full)

for ax, segs in zip([axD1, axD2], [full, pruned]):
    for s in segs:
        ax.plot(s[:, 0], s[:, 1], s[:, 2], lw=1.2)
    ax.scatter([soma[0]], [soma[1]], [soma[2]], s=200, c="red")
    ax.set_xlim(150, 400)
    ax.set_ylim(150, 400)
    ax.set_zlim(150, 400)

axD1.view_init(25, -45)
axD2.view_init(25, -25)
axD1.text2D(-0.15, 1.05, "D",
            transform=axD1.transAxes,
            fontsize=16, fontweight="bold")

plt.tight_layout()
plt.show()