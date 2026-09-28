"""The lesson pages quote program output and statistics. Check that they still match the code."""

import re
from pathlib import Path

import numpy as np
import pytest

import ekf_localization as ekf
import kalman_filter_1d as kf

PAGES = Path(__file__).resolve().parents[1] / "docs/start-here"
SCRIPT_FOR_PAGE = {
    "index.md": "bayes_filter_1d.py",
    "1-bayes-filter.md": "bayes_filter_1d.py",
    "2-kalman-filter.md": "kalman_filter_1d.py",
    "3-ekf-localization.md": "ekf_localization.py",
    "4-particle-filter.md": "particle_filter.py",
}


@pytest.mark.parametrize("page, script", SCRIPT_FOR_PAGE.items())
def test_quoted_output_matches_program(page, script, run_example):
    output = {line.rstrip() for line in run_example(script).splitlines()}
    blocks = re.findall(r"```text\n(.*?)```", (PAGES / page).read_text(), flags=re.S)
    assert blocks, f"{page} quotes no program output"
    for block in blocks:
        for line in block.splitlines():
            if line.strip():
                assert line.rstrip() in output, f"{page}: not in {script} output: {line!r}"


def test_kalman_filter_statistics_quoted_in_lesson_2():
    runs = [kf.simulate(seed=s) for s in range(300)]
    rmse = np.array([[kf.rmse(r["truth"], r[k]) for k in ("odometry", "gps", "kf_mean")]
                     for r in runs])
    np.testing.assert_allclose(rmse.mean(axis=0), [1.33, 1.99, 0.59], atol=0.005)
    assert round(100 * np.mean(rmse[:, 2] < rmse[:, 0])) == 92
    inside = np.mean([np.mean(np.abs(r["truth"] - r["kf_mean"]) < 2 * np.sqrt(r["kf_var"]))
                      for r in runs])
    assert round(100 * inside, 1) == 95.9


def test_ekf_statistics_quoted_in_lesson_3():
    inside, rmse, dr, nees, nis = [], [], [], [], []
    for s in range(40):
        r = ekf.simulate(seed=s)
        err = r["truth"] - r["mu"]
        err[:, 2] = ekf.wrap_angle(err[:, 2])
        sigma = np.sqrt(np.diagonal(r["Sigma"], axis1=1, axis2=2))
        inside.append(np.mean(np.abs(err) < 2 * sigma, axis=0))
        rmse.append(ekf.position_rmse(r["truth"], r["mu"]))
        dr.append(ekf.position_rmse(r["truth"], r["dead_reckoning"]))
        nees.append(np.mean([ekf.nees(t, m, S) for t, m, S in zip(r["truth"], r["mu"], r["Sigma"])]))
        nis.append(np.mean(r["nis"]))
    np.testing.assert_array_equal(np.round(100 * np.mean(inside, axis=0)), [95, 94, 95])
    assert round(np.mean(rmse), 2) == 0.09 and round(np.mean(dr), 1) == 1.7
    assert round(np.mean(nees), 2) == 3.15 and round(np.mean(nis), 2) == 1.99
