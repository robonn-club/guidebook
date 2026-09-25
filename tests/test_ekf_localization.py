"""Lesson 3: EKF localization with known landmarks."""

import numpy as np
import pytest

import ekf_localization as ekf

rng = np.random.default_rng(42)
POSES = [np.array([rng.uniform(-10, 10), rng.uniform(-10, 10), th])
         for th in (0.0, 0.7, -2.0, np.pi - 1e-3, -np.pi + 1e-3)]


@pytest.mark.parametrize("x", POSES)
def test_motion_jacobians_match_finite_differences(x):
    u, dt = np.array([1.3, -0.4]), 0.1
    G, V = ekf.motion_jacobians(x, u, dt)
    G_num = ekf.numerical_jacobian(lambda s: ekf.motion_model(s, u, dt), x, angle_rows=[2])
    V_num = ekf.numerical_jacobian(lambda c: ekf.motion_model(x, c, dt), u, angle_rows=[2])
    np.testing.assert_allclose(G, G_num, atol=1e-7)
    np.testing.assert_allclose(V, V_num, atol=1e-7)


@pytest.mark.parametrize("x", POSES)
def test_measurement_jacobian_matches_finite_differences(x):
    landmark = np.array([3.0, -2.0])
    H = ekf.measurement_jacobian(x, landmark)
    H_num = ekf.numerical_jacobian(lambda s: ekf.measurement_model(s, landmark), x,
                                   angle_rows=[1])
    np.testing.assert_allclose(H, H_num, atol=1e-6)


def test_worked_example_matches_lesson():
    ex = ekf.worked_example()
    np.testing.assert_allclose(ex["R"], np.diag([0.01, 0.0, 0.0025]), atol=1e-12)
    np.testing.assert_allclose(ex["mu_bar"], [1.0, 0.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(ex["Sigma_bar"], [[0.05, 0.0, 0.0],
                                                 [0.0, 0.05, 0.01],
                                                 [0.0, 0.01, 0.0125]], atol=1e-12)
    np.testing.assert_allclose(ex["z_hat"], [5.0, 0.6435], atol=5e-5)
    np.testing.assert_allclose(ex["H"], [[-0.8, -0.6, 0.0],
                                         [0.12, -0.16, -1.0]], atol=1e-12)
    np.testing.assert_allclose(ex["nu"], [-0.2, 0.0565], atol=5e-5)
    np.testing.assert_allclose(ex["S"], [[0.06, 0.006], [0.006, 0.0202]], atol=1e-12)
    np.testing.assert_allclose(ex["K"], [[-0.7177, 0.5102],
                                         [-0.4235, -0.7653],
                                         [-0.0311, -0.6888]], atol=5e-5)
    np.testing.assert_allclose(ex["mu"], [1.1724, 0.0415, -0.0327], atol=5e-5)
    np.testing.assert_allclose(ex["Sigma"], [[0.0182, -0.0123, 0.0029],
                                             [-0.0123, 0.0235, -0.0033],
                                             [0.0029, -0.0033, 0.0026]], atol=5e-5)


def test_update_shrinks_uncertainty_and_keeps_covariance_valid():
    ex = ekf.worked_example()
    Sigma = ex["Sigma"]
    np.testing.assert_allclose(Sigma, Sigma.T, atol=1e-15)
    assert np.all(np.linalg.eigvalsh(Sigma) > 0)
    assert np.trace(Sigma) < np.trace(ex["Sigma_bar"])


def test_bearing_innovation_is_wrapped():
    # Robot faces +x, landmark straight behind it: expected bearing is +-pi.
    landmark = np.array([-5.0, 1e-9])
    z = np.array([5.0, -np.pi + 0.01])  # measured just across the +-pi seam
    _, _, nu, _ = ekf.ekf_update(np.zeros(3), np.diag([0.01] * 3), z, landmark,
                                 np.diag([0.01, 0.01]))
    assert abs(nu[1]) < 0.02


def test_ekf_beats_dead_reckoning():
    run = ekf.simulate(seed=0)
    assert ekf.position_rmse(run["truth"], run["mu"]) < 0.2
    assert ekf.position_rmse(run["truth"], run["dead_reckoning"]) > 1.0


def test_filter_is_consistent_over_many_runs():
    runs = [ekf.simulate(seed=s) for s in range(20)]
    nees = np.mean([ekf.nees(t, m, S) for r in runs
                    for t, m, S in zip(r["truth"], r["mu"], r["Sigma"])])
    nis = np.mean(np.concatenate([r["nis"] for r in runs]))
    assert 2.5 < nees < 3.6   # state dimension is 3
    assert 1.8 < nis < 2.2    # measurement dimension is 2


def test_without_measurements_uncertainty_only_grows():
    run = ekf.simulate(steps=200, use_measurements=False)
    traces = np.trace(run["Sigma"], axis1=1, axis2=2)
    assert np.all(np.diff(traces) > 0)


def test_script_runs(run_example):
    assert "position RMSE, EKF" in run_example("ekf_localization.py")
