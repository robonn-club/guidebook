"""Lesson 2 - From histograms to Gaussians: the 1D Kalman filter.

    python kalman_filter_1d.py

A lawn-mower robot drives along a straight 100 m row. Every second it is told
to drive 1 m forward, but its wheels slip on the grass (0.2 m standard
deviation per step). A cheap GPS receiver reports its position with
about 2 m standard deviation. Neither source alone is good enough; the Kalman
filter combines them. Only NumPy is required.
"""

import numpy as np

# --8<-- [start:kf]
def predict(mean, var, u, motion_var):
    """Move by u. The means add, and so do the variances: uncertainty grows."""
    return mean + u, var + motion_var


def update(mean, var, z, meas_var):
    """Fuse a measurement z. The result is more certain than either input."""
    K = var / (var + meas_var)  # Kalman gain, always between 0 and 1
    return mean + K * (z - mean), (1 - K) * var
# --8<-- [end:kf]


# --8<-- [start:simulate]
def simulate(steps=100, seed=0, u=1.0, motion_std=0.2, gps_std=2.0):
    rng = np.random.default_rng(seed)
    truth, odom, gps, kf_mean, kf_var = [], [], [], [], []
    mean, var = 0.0, 0.5**2  # "I am at the start of the row, give or take 0.5 m"
    x_true = rng.normal(mean, np.sqrt(var))
    x_odom = mean

    for _ in range(steps):
        x_true += u + rng.normal(0.0, motion_std)  # the wheels slip a bit
        z = x_true + rng.normal(0.0, gps_std)      # GPS reading

        x_odom += u                                # odometry only: trust the command
        mean, var = predict(mean, var, u, motion_std**2)
        mean, var = update(mean, var, z, gps_std**2)

        truth.append(x_true)
        odom.append(x_odom)
        gps.append(z)
        kf_mean.append(mean)
        kf_var.append(var)
    return {k: np.array(v) for k, v in dict(truth=truth, odometry=odom, gps=gps,
                                           kf_mean=kf_mean, kf_var=kf_var).items()}
# --8<-- [end:simulate]


def worked_example():
    """The numbers used on the lesson page."""
    mean, var = predict(10.0, 0.3**2, 1.0, 0.4**2)  # -> 11.0, 0.25
    K = var / (var + 1.0**2)
    new_mean, new_var = update(mean, var, 12.0, 1.0**2)
    return dict(pred_mean=mean, pred_var=var, K=K, mean=new_mean, var=new_var)


def steady_state_variance(motion_var, meas_var):
    """Posterior variance the filter settles to after many steps."""
    # Solve p = (p + q) r / (p + q + r) for p, with q = motion_var, r = meas_var.
    q, r = motion_var, meas_var
    a = (q + np.sqrt(q * q + 4 * q * r)) / 2  # predicted variance a = p + q
    return a - q


# --8<-- [start:grid_check]
def grid_bayes_filter(z_list, u, motion_std, meas_std, prior_mean, prior_std, dx=0.01):
    """The Lesson 1 histogram filter on a fine grid, with Gaussian motion and sensor models.

    If the Kalman filter really is the Bayes filter for Gaussians, this brute-force
    version must give the same mean and variance.
    """
    x = np.arange(-20.0, 20.0 + len(z_list) * u, dx)
    gauss = lambda d, s: np.exp(-0.5 * (d / s) ** 2)
    belief = gauss(x - prior_mean, prior_std)
    belief /= belief.sum()
    offsets = np.arange(-6 * motion_std, 6 * motion_std + dx / 2, dx)
    kernel = gauss(offsets, motion_std)
    kernel /= kernel.sum()
    for z in z_list:
        belief = np.roll(belief, int(round(u / dx)))              # shift by u ...
        belief = np.convolve(belief, kernel, mode="same")         # ... and blur
        belief *= gauss(x - z, meas_std)                          # weight by p(z | x)
        belief /= belief.sum()                                    # normalize
    mean = np.sum(x * belief)
    return mean, np.sum((x - mean) ** 2 * belief)
# --8<-- [end:grid_check]


def rmse(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))


def main():
    ex = worked_example()
    print("Worked example")
    print(f"  after predict: mean = {ex['pred_mean']:.2f} m, variance = {ex['pred_var']:.4f} m^2")
    print(f"  Kalman gain K = {ex['K']:.2f}")
    print(f"  after update:  mean = {ex['mean']:.2f} m, variance = {ex['var']:.4f} m^2")

    run = simulate()
    print("\nOne 100 m run            error (RMSE)")
    print(f"  odometry only           {rmse(run['truth'], run['odometry']):.2f} m")
    print(f"  GPS only                {rmse(run['truth'], run['gps']):.2f} m")
    print(f"  Kalman filter           {rmse(run['truth'], run['kf_mean']):.2f} m")
    print(f"  filter's own std at the end: {np.sqrt(run['kf_var'][-1]):.2f} m "
          f"(steady state {np.sqrt(steady_state_variance(0.2**2, 2.0**2)):.2f} m)")

    print("\nThe same problem as a brute-force histogram filter (Lesson 1) on a 1 cm grid:")
    zs = run["gps"][:10]
    mean_kf, var_kf = 0.0, 0.5**2
    for z in zs:
        mean_kf, var_kf = update(*predict(mean_kf, var_kf, 1.0, 0.2**2), z, 2.0**2)
    mean_grid, var_grid = grid_bayes_filter(zs, 1.0, 0.2, 2.0, 0.0, 0.5)
    print(f"  Kalman filter:  mean {mean_kf:.4f} m, variance {var_kf:.5f} m^2")
    print(f"  histogram:      mean {mean_grid:.4f} m, variance {var_grid:.5f} m^2")


if __name__ == "__main__":
    main()
