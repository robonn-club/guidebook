"""Lesson 4: particle-filter global localization with unlabelled poles."""

import numpy as np

import ekf_localization as ekf
import particle_filter as pf


def test_motion_model_works_on_all_particles_at_once():
    rng = np.random.default_rng(0)
    particles = pf.uniform_particles(50, rng)
    u = np.array([1.0, 0.3])[:, None] + 0.1 * rng.standard_normal((2, 50))
    moved = ekf.motion_model(particles, u, 0.1)
    one_by_one = np.column_stack([ekf.motion_model(particles[:, i], u[:, i], 0.1)
                                  for i in range(50)])
    np.testing.assert_allclose(moved, one_by_one)


def test_likelihood_with_one_pole_is_the_gaussian_log_likelihood():
    particles = np.array([[0.0, 1.0], [0.0, 0.0], [0.0, 0.1]])
    landmark, Q = np.array([5.0, 3.0]), np.diag([0.04, 0.01])
    z = np.array([5.5, 0.5])
    expected = []
    for x in particles.T:
        d = z - ekf.measurement_model(x, landmark)
        expected.append(-0.5 * d @ np.linalg.solve(Q, d))
    np.testing.assert_allclose(pf.log_likelihood(particles, z, [landmark], Q), expected)


def test_bearing_difference_is_wrapped():
    # Pole straight behind the particle: predicted bearing is +pi, reading says -pi + 0.01.
    particle = np.array([[0.0], [0.0], [0.0]])
    landmark, Q = np.array([-5.0, 1e-9]), np.diag([0.04, 0.01])
    z = np.array([5.0, -np.pi + 0.01])
    assert pf.log_likelihood(particle, z, [landmark], Q)[0] > -0.1


def test_normalize_survives_tiny_likelihoods():
    w = pf.normalize(np.array([-1e5, -1e5 + 1.0, -1e5 + 2.0]))
    assert np.all(np.isfinite(w)) and np.isclose(w.sum(), 1.0)
    assert np.argmax(w) == 2


def test_low_variance_resampling_copies_in_proportion_to_weight():
    rng = np.random.default_rng(1)
    particles = np.arange(12.0).reshape(3, 4)
    weights = np.array([0.5, 0.25, 0.25, 0.0])
    counts = np.bincount(pf.low_variance_resample(particles, weights, rng)[0].astype(int),
                         minlength=4)
    np.testing.assert_array_equal(counts, [2, 1, 1, 0])


def test_effective_sample_size_limits():
    assert np.isclose(pf.effective_sample_size(np.full(100, 0.01)), 100)
    assert np.isclose(pf.effective_sample_size(np.eye(1, 100)[0]), 1)


def test_default_run_localizes_the_robot():
    run = pf.simulate(seed=0)
    assert run["errors"][0] > run["errors"][-1]
    assert run["errors"][-1] < 0.3


def test_particle_filter_localizes_where_the_ekf_guessing_fails():
    wide = np.diag([24**2 / 12, 34**2 / 12, (2 * np.pi)**2 / 12])
    guesses = np.random.default_rng(99)
    ekf_ok = sum(pf.ekf_with_guess(pf.uniform_particles(1, guesses)[:, 0], wide, s)[-1] < 0.5
                 for s in range(8))
    pf_ok = sum(pf.simulate(2000, seed=s)["errors"][-1] < 0.5 for s in range(8))
    assert pf_ok == 8
    assert ekf_ok < pf_ok


def test_roughening_helps_with_few_particles():
    plain = sum(pf.simulate(200, roughen_std=None, seed=s)["errors"][-1] < 0.5 for s in range(12))
    rough = sum(pf.simulate(200, seed=s)["errors"][-1] < 0.5 for s in range(12))
    assert rough > plain


def test_script_runs(run_example):
    assert "Global localization" in run_example("particle_filter.py")
