"""Lesson 2: the 1D Kalman filter."""

import numpy as np

import kalman_filter_1d as kf


def test_worked_example_matches_lesson():
    ex = kf.worked_example()
    assert np.isclose(ex["pred_mean"], 11.0) and np.isclose(ex["pred_var"], 0.25)
    assert np.isclose(ex["K"], 0.2)
    assert np.isclose(ex["mean"], 11.2) and np.isclose(ex["var"], 0.2)


def test_fused_estimate_is_more_certain_than_either_input():
    for var, meas_var in [(0.25, 1.0), (4.0, 0.1), (1.0, 1.0)]:
        _, new_var = kf.update(0.0, var, 1.0, meas_var)
        assert new_var < min(var, meas_var)


def test_kalman_filter_equals_brute_force_bayes_filter():
    zs = kf.simulate(steps=10, seed=3)["gps"]
    mean, var = 0.0, 0.5**2
    for z in zs:
        mean, var = kf.update(*kf.predict(mean, var, 1.0, 0.2**2), z, 2.0**2)
    grid_mean, grid_var = kf.grid_bayes_filter(zs, 1.0, 0.2, 2.0, 0.0, 0.5)
    assert abs(mean - grid_mean) < 1e-3
    assert abs(var - grid_var) < 1e-3


def test_steady_state_variance_formula():
    var = 0.25
    for _ in range(500):
        var = kf.update(*kf.predict(0.0, var, 0.0, 0.2**2), 0.0, 2.0**2)[1]
    assert np.isclose(var, kf.steady_state_variance(0.2**2, 2.0**2))


def test_filter_beats_both_sensors_and_is_consistent():
    runs = [kf.simulate(seed=s) for s in range(200)]
    rmse = np.array([[kf.rmse(r["truth"], r[k]) for k in ("odometry", "gps", "kf_mean")]
                     for r in runs]).mean(axis=0)
    assert rmse[2] < rmse[0] and rmse[2] < rmse[1]
    inside = np.mean([np.mean(np.abs(r["truth"] - r["kf_mean"]) < 2 * np.sqrt(r["kf_var"]))
                      for r in runs])
    assert 0.94 < inside < 0.97  # a Gaussian has 95.4 % of its mass within 2 sigma


def test_script_runs(run_example):
    assert "Kalman filter" in run_example("kalman_filter_1d.py")
