"""EKF localization of a wheeled robot with known range-bearing landmarks.

Lesson 3 of the guidebook's Start Here path: "Localizing a real robot: the EKF".
Only NumPy is required:

    python ekf_localization.py            # worked example, then one simulated lap
    python ekf_localization.py --seed 3   # a different lap

Notation follows Probabilistic Robotics (Thrun, Burgard, Fox):
    mu, Sigma   belief mean and covariance, state = [x, y, theta]
    u           control / odometry reading = [v, omega]
    M           control noise covariance (noise on v and omega)
    R           motion noise covariance in *state* space
    Q           measurement noise covariance
"""

import argparse

import numpy as np


# --8<-- [start:wrap]
def wrap_angle(a):
    """Map an angle (or array of angles) to [-pi, pi)."""
    return (a + np.pi) % (2 * np.pi) - np.pi
# --8<-- [end:wrap]


# --8<-- [start:motion]
def motion_model(x, u, dt):
    """Unicycle model, one Euler step. x = [x, y, theta], u = [v, omega]."""
    px, py, theta = x
    v, omega = u
    return np.array([
        px + v * dt * np.cos(theta),
        py + v * dt * np.sin(theta),
        wrap_angle(theta + omega * dt),
    ])


def motion_jacobians(x, u, dt):
    """G = dg/dx (3x3) and V = dg/du (3x2), evaluated at (x, u)."""
    theta = x[2]
    v = u[0]
    G = np.array([
        [1.0, 0.0, -v * dt * np.sin(theta)],
        [0.0, 1.0,  v * dt * np.cos(theta)],
        [0.0, 0.0,  1.0],
    ])
    V = np.array([
        [dt * np.cos(theta), 0.0],
        [dt * np.sin(theta), 0.0],
        [0.0,                dt],
    ])
    return G, V
# --8<-- [end:motion]


# --8<-- [start:measurement]
def measurement_model(x, landmark):
    """Expected range and bearing from pose x to a landmark at [mx, my]."""
    dx = landmark[0] - x[0]
    dy = landmark[1] - x[1]
    return np.array([
        np.hypot(dx, dy),
        wrap_angle(np.arctan2(dy, dx) - x[2]),
    ])


def measurement_jacobian(x, landmark):
    """H = dh/dx (2x3), evaluated at pose x."""
    dx = landmark[0] - x[0]
    dy = landmark[1] - x[1]
    q = dx**2 + dy**2
    r = np.sqrt(q)
    return np.array([
        [-dx / r, -dy / r,  0.0],
        [ dy / q, -dx / q, -1.0],
    ])
# --8<-- [end:measurement]


# --8<-- [start:numerical_jacobian]
def numerical_jacobian(f, x, eps=1e-6, angle_rows=()):
    """Central-difference Jacobian of f at x.

    Compare it against every analytical Jacobian you write. `angle_rows`
    lists output components that are angles, so a difference that straddles
    +-pi is wrapped instead of showing up as a 2*pi jump.
    """
    x = np.asarray(x, dtype=float)
    columns = []
    for i in range(x.size):
        step = np.zeros_like(x)
        step[i] = eps
        diff = np.asarray(f(x + step)) - np.asarray(f(x - step))
        for row in angle_rows:
            diff[row] = wrap_angle(diff[row])
        columns.append(diff / (2 * eps))
    return np.column_stack(columns)
# --8<-- [end:numerical_jacobian]


# --8<-- [start:predict]
def ekf_predict(mu, Sigma, u, M, dt):
    G, V = motion_jacobians(mu, u, dt)  # linearize at the current estimate
    R = V @ M @ V.T                     # control noise mapped into state space
    mu_bar = motion_model(mu, u, dt)
    Sigma_bar = G @ Sigma @ G.T + R
    return mu_bar, Sigma_bar
# --8<-- [end:predict]


# --8<-- [start:update]
def ekf_update(mu_bar, Sigma_bar, z, landmark, Q):
    H = measurement_jacobian(mu_bar, landmark)  # linearize at the prediction
    nu = z - measurement_model(mu_bar, landmark)  # innovation
    nu[1] = wrap_angle(nu[1])                     # 359 deg - 1 deg is -2 deg
    S = H @ Sigma_bar @ H.T + Q                   # innovation covariance
    K = np.linalg.solve(S, H @ Sigma_bar).T       # = Sigma_bar H^T S^-1
    mu = mu_bar + K @ nu
    mu[2] = wrap_angle(mu[2])
    I_KH = np.eye(3) - K @ H
    Sigma = I_KH @ Sigma_bar @ I_KH.T + K @ Q @ K.T  # Joseph form
    return mu, Sigma, nu, S
# --8<-- [end:update]


def nees(x_true, mu, Sigma):
    """Normalized estimation error squared. Averages to 3 for a consistent filter."""
    e = x_true - mu
    e[2] = wrap_angle(e[2])
    return float(e @ np.linalg.solve(Sigma, e))


def worked_example():
    """One predict and one update step with the numbers used on the page."""
    mu = np.array([0.0, 0.0, 0.0])
    Sigma = np.diag([0.04, 0.04, 0.01])
    u = np.array([1.0, 0.0])
    M = np.diag([0.01, 0.0025])
    dt = 1.0
    landmark = np.array([5.0, 3.0])
    z = np.array([4.8, 0.70])
    Q = np.diag([0.01, 0.0025])

    G, V = motion_jacobians(mu, u, dt)
    mu_bar, Sigma_bar = ekf_predict(mu, Sigma, u, M, dt)
    z_hat = measurement_model(mu_bar, landmark)
    H = measurement_jacobian(mu_bar, landmark)
    mu_new, Sigma_new, nu, S = ekf_update(mu_bar, Sigma_bar, z, landmark, Q)
    K = Sigma_bar @ H.T @ np.linalg.inv(S)
    return dict(G=G, V=V, R=V @ M @ V.T, mu_bar=mu_bar, Sigma_bar=Sigma_bar,
                z_hat=z_hat, H=H, nu=nu, S=S, K=K, mu=mu_new, Sigma=Sigma_new)


# --8<-- [start:simulate]
LANDMARKS = np.array([  # poles at known map positions; deliberately not symmetric
    [ 0.0, -4.0], [ 9.0,  3.0], [ 5.0, 21.0],
    [ 0.0, 24.0], [-9.0, 17.0], [-9.0,  3.0],
])


def simulate(steps=630, dt=0.1, seed=0, use_measurements=True):
    """Drive one lap of a circle; return truth, EKF and dead-reckoning results."""
    rng = np.random.default_rng(seed)
    u_cmd = np.array([1.0, 0.1])             # 1 m/s, 0.1 rad/s -> radius 10 m
    M = np.diag([0.1**2, 0.05**2])            # odometry noise on v and omega
    Q = np.diag([0.2**2, np.deg2rad(3)**2])   # range and bearing noise
    max_range, measure_every = 12.0, 5        # sensor sees 12 m, runs at 2 Hz

    x_true = np.array([0.0, 0.0, 0.0])
    Sigma = np.diag([0.1**2, 0.1**2, np.deg2rad(5)**2])
    mu = x_true + np.linalg.cholesky(Sigma) @ rng.standard_normal(3)
    x_dr = mu.copy()                          # dead reckoning: odometry only

    log = {k: [] for k in ("truth", "mu", "Sigma", "dead_reckoning", "nis")}
    for k in range(steps):
        x_true = motion_model(x_true, u_cmd, dt)
        u_odom = u_cmd + np.linalg.cholesky(M) @ rng.standard_normal(2)
        mu, Sigma = ekf_predict(mu, Sigma, u_odom, M, dt)
        x_dr = motion_model(x_dr, u_odom, dt)

        if use_measurements and k % measure_every == 0:
            for landmark in LANDMARKS:
                z = measurement_model(x_true, landmark)
                if z[0] > max_range:
                    continue
                z = z + np.linalg.cholesky(Q) @ rng.standard_normal(2)
                z[1] = wrap_angle(z[1])
                mu, Sigma, nu, S = ekf_update(mu, Sigma, z, landmark, Q)
                log["nis"].append(float(nu @ np.linalg.solve(S, nu)))

        log["truth"].append(x_true)
        log["mu"].append(mu)
        log["Sigma"].append(Sigma)
        log["dead_reckoning"].append(x_dr)
    return {k: np.array(v) for k, v in log.items()} | {"dt": dt}
# --8<-- [end:simulate]


def position_rmse(truth, estimate):
    return float(np.sqrt(np.mean(np.sum((truth[:, :2] - estimate[:, :2])**2, axis=1))))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=9, help="which simulated run (9 is typical)")
    args = parser.parse_args()
    np.set_printoptions(precision=4, suppress=True)
    ex = worked_example()
    print("Worked example")
    for name in ("mu_bar", "Sigma_bar", "z_hat", "H", "nu", "S", "K", "mu", "Sigma"):
        print(f"{name} =\n{ex[name]}\n")

    run = simulate(seed=args.seed)
    ekf_err = position_rmse(run["truth"], run["mu"])
    dr_err = position_rmse(run["truth"], run["dead_reckoning"])
    mean_nees = np.mean([nees(t, m, S) for t, m, S in
                         zip(run["truth"], run["mu"], run["Sigma"])])
    print("One lap of simulation")
    print(f"  position RMSE, dead reckoning: {dr_err:.2f} m")
    print(f"  position RMSE, EKF:            {ekf_err:.2f} m")
    print(f"  mean NEES (expect about 3):    {mean_nees:.2f}")
    print(f"  mean NIS  (expect about 2):    {np.mean(run['nis']):.2f}")


if __name__ == "__main__":
    main()
