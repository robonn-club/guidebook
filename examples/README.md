# Examples

Runnable code for the [Start Here](https://robonn-club.github.io/guidebook/start-here/) lessons.
Each file is short, needs only NumPy, and prints what it is doing.

| Lesson | File | What it shows |
|---|---|---|
| 1 | `bayes_filter_1d.py` | A robot in a hallway works out where it is from "door" / "wall" readings |
| 2 | `kalman_filter_1d.py` | Fusing wheel odometry and GPS with two lines of math |
| 3 | `ekf_localization.py` | A wheeled robot localizes itself in 2D from range-bearing measurements |
| 4 | `particle_filter.py` | Finding the robot with no initial guess and look-alike landmarks |

## Run them

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r examples/requirements.txt
python examples/bayes_filter_1d.py
```

The lesson pages embed these exact files, and `tests/` checks that they behave as the lessons
claim. After changing an example, run `pip install pytest && pytest tests`.
