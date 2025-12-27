# SynapFlow

**SynapFlow** is a numerical simulation project focused on modeling neural and nerve dynamics using simplified mathematical neuron models.

The code generates a multi-panel figure (A–D) illustrating different biological scenarios:
- populations of pyramidal-like neurons,
- a single highly branched neuron,
- axon / cable bundle geometry in 3D,
- pruning of neuronal arbors.

The implementation is **manual and independent** — it does **not** use NeuroDevSim or any other external neuron-growth framework.

<img width="1065" height="643" alt="Figure 2025-12-27 205325" src="https://github.com/user-attachments/assets/22c1edc1-cb03-4eaf-afe1-f7408cb47b23" />

---

## Scientific Background

The modeling approach is **inspired by concepts and visual targets** presented in the following publication:

> **Zubler et al., 2023**  
> *NeuroDevSim: a Python-based framework for neuronal development simulations*  
> Frontiers in Neuroinformatics  
> https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2023.1212384/full

This repository **does not reproduce or reuse the original code** from the paper.  
Instead, it implements a **simplified, custom stochastic growth model** designed to approximate similar qualitative behaviors and visual structures.

---

## Model Overview

### Growth Principles
- Neurites grow as 3D stochastic trajectories with:
  - small transverse noise,
  - directional persistence,
  - probabilistic branching.
- Branching is implemented **recursively**, allowing multi-level arborization.
- Growth is step-based (fixed spatial increments), not time-based.

### Panels Generated

**A — Neuronal Population**  
A row of pyramidal-like neurons with:
- apical trunks,
- dense apical tufts,
- basal dendritic trees.

**B — Single Neuron**  
A highly branched neuron visualized in 2D projection.

**C — Axon / Cable Bundle**  
Multiple parallel cable-like trajectories:
- each with its own soma (gray marker),
- markers placed approximately at mid-cable positions,
- slight directional variability to avoid overlap.

**D — Pruning Example**  
Comparison between:
- a full recursive arbor,
- a pruned version retaining only a fraction of branches.

---

## Implementation Details

- Language: **Python 3**
- Dependencies:
  - `numpy`
  - `matplotlib`
- No external neuroscience libraries required.
- All geometry is generated procedurally at runtime.

Key components:
- `grow_trunk()` — straight but noisy growth
- `grow_branch()` — branching growth with probabilistic side branches
- `recursive_branch()` — multi-depth arborization
- `pyramidal_neuron()` — composite neuron model
- `cable_bundle()` — axon bundle generation
- `prune()` — simple structural pruning

---

## Mathematical Model

Neurite growth is modeled as a discrete stochastic process in 3D space.
Each growing process is described by a position vector and a unit direction.

### Direction normalization

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\| + \varepsilon}
$$

### Transverse noise

Noise is added only perpendicular to the current direction:

$$
\mathbf{r}_\perp = \mathbf{r} - (\mathbf{r}\cdot \hat{\mathbf{d}})\hat{\mathbf{d}},
\quad \mathbf{r} \sim \mathcal{N}(0, I)
$$

$$
\hat{\mathbf{d}}_{k+1} =
\frac{\hat{\mathbf{d}}_k + \sigma \mathbf{r}_\perp}
{\|\hat{\mathbf{d}}_k + \sigma \mathbf{r}_\perp\|}
$$

### Position update

$$
\mathbf{x}_{k+1} = \mathbf{x}_k + s \hat{\mathbf{d}}_{k+1}
$$




Simply execute:

```bash
python model.py
