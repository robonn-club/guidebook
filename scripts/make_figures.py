"""Regenerate the figures on the Start Here lesson pages.

    pip install numpy matplotlib
    python scripts/make_figures.py

Writes light- and dark-theme SVGs to docs/start-here/assets/.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
import ekf_localization as ekf  # noqa: E402
import kalman_filter_1d as kf  # noqa: E402
import particle_filter as pf  # noqa: E402

ASSETS = ROOT / "docs/start-here/assets"
EKF_SEED = 9   # a typical run: error inside the 2-sigma band ~95 % of the time

THEMES = {
    "light": dict(ink="#131313", muted="#485F66", grid="#d3dce2", sample="#7a8f98",
                  blue="#2a78d6", orange="#eb6834", aqua="#1baf7a"),
    "dark": dict(ink="#ECF1F5", muted="#a0b3bb", grid="#2e3d43", sample="#8fa3ab",
                 blue="#3987e5", orange="#d95926", aqua="#199e70"),
}


def style(theme):
    c = THEMES[theme]
    plt.rcParams.update({
        "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",
        "text.color": c["ink"], "axes.labelcolor": c["ink"], "axes.edgecolor": c["grid"],
        "xtick.color": c["muted"], "ytick.color": c["muted"],
        "axes.grid": True, "grid.color": c["grid"], "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "lines.linewidth": 2, "lines.solid_capstyle": "round",
        "legend.frameon": False, "font.size": 10, "svg.hashsalt": "guidebook",
    })
    return c


def save(fig, name, theme):
    fig.savefig(ASSETS / f"{name}-{theme}.svg", dpi=200, metadata={"Date": None},
                bbox_inches="tight")
    plt.close(fig)


def ellipse(mean, cov, n_sigma, **kwargs):
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    w, h = 2 * n_sigma * np.sqrt(vals[::-1])
    return Ellipse(mean, w, h, angle=angle, fill=False, **kwargs)


# ------------------------------------------------------------------ Lesson 2

def kf_run_figure(theme):
    c = style(theme)
    run = kf.simulate(seed=0)
    t = np.arange(1, run["truth"].size + 1)
    err = lambda key: run[key] - run["truth"]
    band = 2 * np.sqrt(run["kf_var"])

    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.fill_between(t, -band, band, color=c["blue"], alpha=0.12, lw=0)
    ax.plot(t, err("gps"), "o", ms=3, color=c["orange"], mec="none", label="GPS only")
    ax.plot(t, err("odometry"), color=c["aqua"], ls=(0, (5, 3)), label="Odometry only")
    ax.plot(t, err("kf_mean"), color=c["blue"], label="Kalman filter (band: ±2σ)")
    ax.axhline(0, color=c["ink"], lw=1)
    ax.set_xlabel("step (1 m per step)")
    ax.set_ylabel("error vs. true position [m]")
    ax.legend(loc="lower left", ncol=3, bbox_to_anchor=(0, 1.0), fontsize=9)
    save(fig, "kf_run", theme)


# ------------------------------------------------------------------ Lesson 3

def ekf_linearization_figure(theme):
    """Push a pose with uncertain heading through the motion model."""
    c = style(theme)
    rng = np.random.default_rng(1)
    mu = np.array([0.0, 0.0, 0.0])
    Sigma = np.diag([0.05**2, 0.05**2, np.deg2rad(25)**2])
    u, dt = np.array([4.0, 0.0]), 1.0

    samples = rng.multivariate_normal(mu, Sigma, 1500)
    moved = np.array([ekf.motion_model(s, u, dt) for s in samples])[:, :2]
    mc_mean, mc_cov = moved.mean(axis=0), np.cov(moved.T)
    G, _ = ekf.motion_jacobians(mu, u, dt)
    ekf_mean = ekf.motion_model(mu, u, dt)[:2]
    ekf_cov = (G @ Sigma @ G.T)[:2, :2]

    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.scatter(moved[:, 0], moved[:, 1], s=4, color=c["sample"], alpha=0.45, linewidths=0,
               rasterized=True, label="Where the robot really ends up (1,500 samples)")
    ax.add_patch(ellipse(mc_mean, mc_cov, 2, color=c["ink"], lw=2, ls=(0, (4, 3)),
                         label="Best Gaussian for those samples (2σ)"))
    ax.add_patch(ellipse(ekf_mean, ekf_cov, 2, color=c["blue"], lw=2,
                         label="EKF prediction (2σ)"))
    ax.plot(*mc_mean, "o", ms=7, color=c["ink"], mec="none")
    ax.plot(*ekf_mean, "o", ms=7, color=c["blue"], mec="none")
    ax.annotate("true mean", mc_mean, xytext=(-8, 16), textcoords="offset points",
                ha="right", color=c["ink"])
    ax.annotate("EKF mean", ekf_mean, xytext=(10, -14), textcoords="offset points",
                color=c["ink"])
    ax.plot(0, 0, marker=(3, 0, -90), ms=12, color=c["ink"])
    ax.annotate("start\nheading ±25°", (0, 0), xytext=(0, -30), textcoords="offset points",
                ha="center", color=c["muted"])
    ax.set_aspect("equal")
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-3.2, 3.2)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=9)
    save(fig, "ekf_linearization", theme)


def ekf_trajectory_figure(theme, run):
    c = style(theme)
    fig, ax = plt.subplots(figsize=(6.4, 6))
    truth, est, dr = run["truth"], run["mu"], run["dead_reckoning"]
    ax.plot(truth[:, 0], truth[:, 1], color=c["ink"], label="Ground truth")
    ax.plot(dr[:, 0], dr[:, 1], color=c["orange"], ls=(0, (5, 3)),
            label="Dead reckoning (odometry only)")
    ax.plot(est[:, 0], est[:, 1], color=c["blue"], label="EKF estimate")
    ax.plot(ekf.LANDMARKS[:, 0], ekf.LANDMARKS[:, 1], "^", ms=10, color=c["aqua"],
            mec="none", label="Poles (known map)")
    ax.plot(*truth[0, :2], "o", ms=7, color=c["ink"])
    ax.annotate("start", truth[0, :2], xytext=(6, 8), textcoords="offset points", color=c["ink"])
    ax.annotate("dead reckoning\nafter one lap", dr[-1, :2], xytext=(-20, -34),
                textcoords="offset points", color=c["ink"], ha="right",
                arrowprops=dict(arrowstyle="-", color=c["muted"], lw=1))
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.legend(loc="center", fontsize=9)
    save(fig, "ekf_trajectory", theme)


def ekf_consistency_figure(theme, run):
    c = style(theme)
    t = np.arange(len(run["truth"])) * run["dt"]
    err = run["truth"] - run["mu"]
    err[:, 2] = ekf.wrap_angle(err[:, 2])
    sigma = np.sqrt(np.diagonal(run["Sigma"], axis1=1, axis2=2))
    scale = [1.0, 1.0, np.degrees(1.0)]
    labels = ["x error [m]", "y error [m]", "θ error [deg]"]

    fig, axes = plt.subplots(3, 1, figsize=(7, 6), sharex=True)
    for i, ax in enumerate(axes):
        bound = 2 * sigma[:, i] * scale[i]
        ax.fill_between(t, -bound, bound, color=c["blue"], alpha=0.12, lw=0)
        ax.plot(t, bound, color=c["blue"], lw=1)
        ax.plot(t, -bound, color=c["blue"], lw=1)
        ax.plot(t, err[:, i] * scale[i], color=c["ink"], lw=1.2)
        ax.set_ylabel(labels[i])
    axes[0].plot([], [], color=c["ink"], lw=1.2, label="Actual error (truth − estimate)")
    axes[0].fill_between([], [], [], color=c["blue"], alpha=0.25, lw=0,
                         label="±2σ, from the filter's own covariance")
    axes[0].legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, fontsize=9)
    axes[-1].set_xlabel("time [s]")
    save(fig, "ekf_consistency", theme)


# ------------------------------------------------------------------ Lesson 4

def pf_snapshots_figure(theme):
    """Uniform prior -> one reading (rings) -> first full scan -> 5 s later.

    The first three panels use 200,000 particles so the rings are visible;
    the filter in particle_filter.py uses 5,000.
    """
    c = style(theme)
    rng = np.random.default_rng(0)
    n = 200_000
    run = list(pf.robot_run(seed=0))
    x0, u0, readings0 = run[0]

    particles = pf.pf_predict(pf.uniform_particles(n, rng), u0, pf.M, pf.DT, rng)
    panels = [("Before any reading:\n\"I could be anywhere\"", particles, np.full(n, 1 / n))]
    log_w = pf.log_likelihood(particles, readings0[0], ekf.LANDMARKS, pf.Q)
    panels.append(("After ONE pole reading:\na ring around every pole",
                   particles, pf.normalize(log_w)))
    for z in readings0[1:]:
        log_w += pf.log_likelihood(particles, z, ekf.LANDMARKS, pf.Q)
    panels.append((f"After the first scan\n({len(readings0)} poles in view)",
                   particles, pf.normalize(log_w)))

    sim = pf.simulate(seed=0, snapshot_steps=(50,))
    snap = sim["snapshots"][50]
    panels.append(("5 s later: one tight cluster\nthat follows the robot",
                   snap["particles"], snap["weights"]))
    truths = [x0, x0, x0, snap["truth"]]

    fig, axes = plt.subplots(1, 4, figsize=(11, 4.2), sharey=True)
    for ax, (title, parts, w), truth in zip(axes, panels, truths):
        shown = pf.low_variance_resample(parts, w, np.random.default_rng(1))
        shown = shown[:, np.random.default_rng(2).choice(shown.shape[1], 4000, replace=False)]
        ax.scatter(shown[0], shown[1], s=3, color=c["blue"], alpha=0.5, linewidths=0,
                   rasterized=True)
        ax.plot(ekf.LANDMARKS[:, 0], ekf.LANDMARKS[:, 1], "^", ms=8, color=c["aqua"], mec="none")
        ax.plot(*truth[:2], "o", ms=13, mfc="none", mec=c["ink"], mew=1.5)
        ax.set_title(title, fontsize=9.5, color=c["ink"])
        ax.set_aspect("equal")
        ax.set_xlim(*pf.ARENA[0])
        ax.set_ylim(*pf.ARENA[1])
        ax.set_xticks([-10, 0, 10])
    axes[0].set_ylabel("y [m]")
    axes[0].plot([], [], "o", ms=5, color=c["blue"], label="particles")
    axes[0].plot([], [], "^", ms=8, color=c["aqua"], label="poles (all look alike)")
    axes[0].plot([], [], "o", ms=10, mfc="none", mec=c["ink"], mew=1.5, label="true robot position")
    fig.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.04), fontsize=9)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "pf_snapshots", theme)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    run = ekf.simulate(seed=EKF_SEED)
    for theme in THEMES:
        kf_run_figure(theme)
        ekf_linearization_figure(theme)
        ekf_trajectory_figure(theme, run)
        ekf_consistency_figure(theme, run)
        pf_snapshots_figure(theme)
    print(f"Figures written to {ASSETS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
