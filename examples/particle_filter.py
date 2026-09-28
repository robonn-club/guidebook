"""Lesson 4 - When one Gaussian is not enough: the particle filter.

    python particle_filter.py             # one run, printed step by step
    python particle_filter.py --compare   # the experiments quoted in the lesson (~1 min)

The robot and poles from Lesson 3, with the two conveniences removed:
  * the robot has no idea where it starts (anywhere in the arena, any heading);
  * the poles all look the same, so a reading does not say *which* pole it is.
Only NumPy is required.
"""

import argparse

import numpy as np

from ekf_localization import (LANDMARKS, ekf_predict, ekf_update, measurement_jacobian,
                              measurement_model, motion_model, wrap_angle)

ARENA = ((-12.0, 12.0), (-7.0, 27.0))  # x and y limits in metres


# --8<-- [start:init]
def uniform_particles(n, rng, arena=ARENA):
    """n guesses spread over the whole arena with random headings.

    Particles are stored as a 3 x n array, one column per particle, so the
    Lesson 3 motion_model and measurement_model work on all of them at once.
    """
    (xmin, xmax), (ymin, ymax) = arena
    return np.array([rng.uniform(xmin, xmax, n),
                     rng.uniform(ymin, ymax, n),
                     rng.uniform(-np.pi, np.pi, n)])
# --8<-- [end:init]


# --8<-- [start:predict]
def pf_predict(particles, u, M, dt, rng):
    """Move every particle with its own random draw of the odometry noise."""
    n = particles.shape[1]
    noisy_u = u[:, None] + np.linalg.cholesky(M) @ rng.standard_normal((2, n))
    return motion_model(particles, noisy_u, dt)
# --8<-- [end:predict]


# --8<-- [start:weight]
def log_likelihood(particles, z, landmarks, Q):
    """log p(z | particle) for one range-bearing reading of an unidentified pole.

    The reading could come from any pole, so the likelihood is the average
    over poles: p(z | x) = (1/J) * sum_j p(z | x, pole j).
    """
    per_pole = []
    for landmark in landmarks:
        diff = z[:, None] - measurement_model(particles, landmark)
        diff[1] = wrap_angle(diff[1])
        per_pole.append(-0.5 * np.sum(diff * np.linalg.solve(Q, diff), axis=0))
    per_pole = np.array(per_pole)                      # J x n
    peak = per_pole.max(axis=0)                        # log-sum-exp, safely
    return peak + np.log(np.mean(np.exp(per_pole - peak), axis=0))


def normalize(log_weights):
    """Turn log-weights into weights that sum to one without underflowing."""
    w = np.exp(log_weights - log_weights.max())
    return w / w.sum()
# --8<-- [end:weight]


# --8<-- [start:resample]
def low_variance_resample(particles, weights, rng):
    """Draw n particles in proportion to their weights using one random number.

    Compared with n independent draws this keeps more diversity: a particle
    with weight w is copied either floor(n w) or ceil(n w) times.
    """
    n = weights.size
    positions = (rng.random() + np.arange(n)) / n
    cumulative = np.cumsum(weights)
    cumulative[-1] = 1.0  # guard against rounding
    return particles[:, np.searchsorted(cumulative, positions)]


def effective_sample_size(weights):
    """About n when weights are even, about 1 when one particle has them all."""
    return 1.0 / np.sum(weights**2)
# --8<-- [end:resample]


# --8<-- [start:roughen]
def roughen(particles, std_xy, std_theta, rng):
    """Nudge every particle by a little random noise after resampling.

    Resampling makes exact copies. Without enough noise to pull them apart,
    the cloud can shrink onto a slightly wrong pose and never recover.
    """
    noise = rng.standard_normal(particles.shape) * np.array([[std_xy], [std_xy], [std_theta]])
    moved = particles + noise
    moved[2] = wrap_angle(moved[2])
    return moved
# --8<-- [end:roughen]


def estimate(particles, weights):
    """Weighted mean pose. Only meaningful once the cloud has a single cluster."""
    x, y = particles[0] @ weights, particles[1] @ weights
    theta = np.arctan2(np.sin(particles[2]) @ weights, np.cos(particles[2]) @ weights)
    return np.array([x, y, theta])


def spread(particles, weights):
    """Weighted standard deviation of particle positions, in metres."""
    mean = particles[:2] @ weights
    return float(np.sqrt(np.sum(weights * np.sum((particles[:2] - mean[:, None])**2, axis=0))))


# --8<-- [start:world]
DT, STEPS = 0.1, 400
U_CMD = np.array([1.0, 0.1])                # the Lesson 3 circle
M = np.diag([0.1**2, 0.05**2])              # odometry noise
Q = np.diag([0.2**2, np.deg2rad(3)**2])     # real range and bearing noise
MAX_RANGE, MEASURE_EVERY = 12.0, 5


def robot_run(seed):
    """Yield (odometry, readings) for each step of one run, plus the true pose."""
    rng = np.random.default_rng(seed)
    x_true = np.array([0.0, 0.0, 0.0])
    for k in range(STEPS):
        x_true = motion_model(x_true, U_CMD, DT)
        u_odom = U_CMD + np.linalg.cholesky(M) @ rng.standard_normal(2)
        readings = []
        if k % MEASURE_EVERY == 0:
            for landmark in LANDMARKS:
                z = measurement_model(x_true, landmark)
                if z[0] <= MAX_RANGE:
                    z = z + np.linalg.cholesky(Q) @ rng.standard_normal(2)
                    z[1] = wrap_angle(z[1])
                    readings.append(z)   # no pole ID: just range and bearing
        yield x_true, u_odom, readings
# --8<-- [end:world]


# --8<-- [start:simulate]
def simulate(n_particles=5000, roughen_std=(0.05, np.deg2rad(1)), seed=0, snapshot_steps=()):
    """Global localization with a particle filter.

    roughen_std: (metres, radians) of jitter after resampling; None to disable.
    """
    rng = np.random.default_rng(seed + 10_000)  # the filter's own randomness
    particles = uniform_particles(n_particles, rng)
    log_w = np.zeros(n_particles)
    errors, spreads, snapshots = [], [], {}

    for k, (x_true, u_odom, readings) in enumerate(robot_run(seed)):
        particles = pf_predict(particles, u_odom, M, DT, rng)
        for z in readings:
            log_w += log_likelihood(particles, z, LANDMARKS, Q)
        if readings:
            weights = normalize(log_w)
            if effective_sample_size(weights) < n_particles / 2:
                particles = low_variance_resample(particles, weights, rng)
                log_w = np.zeros(n_particles)
                if roughen_std is not None:
                    particles = roughen(particles, *roughen_std, rng)

        weights = normalize(log_w)
        est = estimate(particles, weights)
        errors.append(np.hypot(*(est[:2] - x_true[:2])))
        spreads.append(spread(particles, weights))
        if k in snapshot_steps:
            snapshots[k] = dict(particles=particles.copy(), weights=weights, truth=x_true)
    return dict(errors=np.array(errors), spreads=np.array(spreads), snapshots=snapshots)
# --8<-- [end:simulate]


def ekf_with_guess(mu, Sigma, seed):
    """The Lesson 3 EKF on the same run. With unlabelled poles it must guess which
    pole it sees: it picks the one closest to its prediction (nearest neighbour)."""
    errors = []
    for x_true, u_odom, readings in robot_run(seed):
        mu, Sigma = ekf_predict(mu, Sigma, u_odom, M, DT)
        for z in readings:
            def distance(landmark):
                H = measurement_jacobian(mu, landmark)
                nu = z - measurement_model(mu, landmark)
                nu[1] = wrap_angle(nu[1])
                return nu @ np.linalg.solve(H @ Sigma @ H.T + Q, nu)
            nearest = min(LANDMARKS, key=distance)
            mu, Sigma, _, _ = ekf_update(mu, Sigma, z, nearest, Q)
        errors.append(np.hypot(*(mu[:2] - x_true[:2])))
    return np.array(errors)


def compare(runs=20):
    """The experiments quoted in the lesson."""
    ok = lambda errors: errors[-1] < 0.5
    print(f"Runs (out of {runs}) that end within 0.5 m of the truth")

    good = sum(ok(ekf_with_guess(np.zeros(3), np.diag([0.1**2, 0.1**2, np.deg2rad(5)**2]), s))
               for s in range(runs))
    guess_rng = np.random.default_rng(99)
    wide = np.diag([24**2 / 12, 34**2 / 12, (2 * np.pi)**2 / 12])  # spread of "anywhere"
    random_start = sum(ok(ekf_with_guess(uniform_particles(1, guess_rng)[:, 0], wide, s))
                       for s in range(runs))
    print(f"  EKF, good initial guess                  {good:3d}")
    print(f"  EKF, random initial guess                {random_start:3d}")
    for n in (200, 500, 1000, 5000):
        plain = sum(ok(simulate(n, roughen_std=None, seed=s)["errors"]) for s in range(runs))
        rough = sum(ok(simulate(n, seed=s)["errors"]) for s in range(runs))
        print(f"  particle filter, {n:5d} particles: {plain:3d} without roughening, {rough:3d} with")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--compare", action="store_true",
                        help="run the experiments quoted in the lesson (about 1 minute)")
    args = parser.parse_args()
    if args.compare:
        compare()
        return

    run = simulate(seed=args.seed)
    print("Global localization with 5,000 particles, unlabelled poles")
    print("   time   position error   particle spread")
    for k in (0, 5, 10, 20, 50, 100, 200, 399):
        print(f"  {k * DT:5.1f} s   {run['errors'][k]:10.2f} m   {run['spreads'][k]:10.2f} m")


if __name__ == "__main__":
    main()
