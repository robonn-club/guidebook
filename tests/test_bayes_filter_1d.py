"""Lesson 1: the discrete Bayes filter in a hallway."""

import numpy as np

import bayes_filter_1d as bf


def test_worked_example_matches_lesson():
    b1, b2, b3 = bf.worked_example()
    np.testing.assert_allclose(b1, np.array([4, 1, 4, 1, 1]) / 11)
    np.testing.assert_allclose(b2, np.array([1.3, 3.4, 1.6, 3.4, 1.3]) / 11)
    np.testing.assert_allclose(b3, np.array([0.26, 2.72, 0.32, 2.72, 1.04]) / 7.06)


def test_predict_keeps_total_probability_and_shifts():
    rng = np.random.default_rng(0)
    belief = rng.random(20)
    belief /= belief.sum()
    assert np.isclose(bf.predict(belief, bf.MOVE_KERNEL).sum(), 1.0)
    np.testing.assert_allclose(bf.predict(belief, np.array([0.0, 1.0, 0.0])), np.roll(belief, 1))


def test_predict_never_sharpens_the_belief():
    belief = np.zeros(20)
    belief[5] = 1.0
    assert bf.predict(belief, bf.MOVE_KERNEL).max() < belief.max()


def test_update_normalizes_and_favours_matching_cells():
    belief = bf.update(np.full(20, 0.05), bf.HALLWAY, bf.DOOR, 0.9)
    assert np.isclose(belief.sum(), 1.0)
    assert belief[bf.HALLWAY == bf.DOOR].min() > belief[bf.HALLWAY == bf.WALL].max()


def test_step_12_of_the_default_run_splits_three_ways():
    # The lesson walks through this step: the robot slipped (stayed in door cell 5)
    # and sensed a door; the belief splits about 26 / 46 / 26 over cells 5, 6, 7.
    step = list(bf.simulate(15, seed=8))[12]
    assert step["true_cell"] == 5 and step["z"] == bf.DOOR
    np.testing.assert_allclose(step["belief"][[5, 6, 7]], [0.26, 0.455, 0.258], atol=0.005)


def test_filter_is_calibrated():
    # When the filter says "70 % sure", it should be right about 70 % of the time.
    confidence, correct = [], []
    for seed in range(400):
        last = list(bf.simulate(15, seed))[-1]
        best = np.argmax(last["belief"])
        confidence.append(last["belief"][best])
        correct.append(best == last["true_cell"])
    assert abs(np.mean(confidence) - np.mean(correct)) < 0.05


def test_script_runs(run_example):
    assert "most likely cell" in run_example("bayes_filter_1d.py")
