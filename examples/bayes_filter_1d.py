"""Lesson 1 - Where am I? A robot in a hallway (the discrete Bayes filter).

    python bayes_filter_1d.py            # watch the belief step by step
    python bayes_filter_1d.py --seed 3   # a different run

The hallway is a loop of 20 cells and some cells have a door. The robot does
not know where it starts. Each step it senses "door" or "wall" (correct 90 %
of the time) and then tries to move one cell forward (it moves exactly one
cell 90 % of the time, stays put 5 %, overshoots by one cell 5 %).
Only NumPy is required.
"""

import argparse

import numpy as np

# --8<-- [start:world]
DOOR, WALL = 1, 0
HALLWAY = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 0,
                    0, 0, 0, 1, 0, 1, 1, 1, 1, 0])  # 1 = door; cell 19 joins cell 0
P_CORRECT = 0.9                           # the sensor is right 90 % of the time
MOVE_KERNEL = np.array([0.05, 0.9, 0.05])  # P(moved 0, 1, 2 cells | told "move 1")
# --8<-- [end:world]


# --8<-- [start:update]
def update(belief, hallway, z, p_correct):
    """Correction step: weight each cell by how well it explains z, then normalize."""
    likelihood = np.where(hallway == z, p_correct, 1 - p_correct)  # p(z | x)
    posterior = likelihood * belief
    return posterior / posterior.sum()
# --8<-- [end:update]


# --8<-- [start:predict]
def predict(belief, kernel):
    """Prediction step: shift the belief by every possible motion, weighted by its probability.

    kernel[k] is the probability of actually moving k cells. np.roll shifts
    the array around the loop, so cell i receives belief[i - k].
    """
    prior = np.zeros_like(belief)
    for k, p_move in enumerate(kernel):
        prior += p_move * np.roll(belief, k)
    return prior
# --8<-- [end:predict]


def worked_example():
    """The five-cell example worked by hand on the lesson page.

    It uses a noisier robot than the main simulation (80 % sensor, 10 % slip
    either way) so the fractions stay easy to compute by hand.
    """
    hallway = np.array([DOOR, WALL, DOOR, WALL, WALL])
    belief0 = np.full(5, 0.2)
    belief1 = update(belief0, hallway, DOOR, 0.8)
    belief2 = predict(belief1, np.array([0.1, 0.8, 0.1]))
    belief3 = update(belief2, hallway, WALL, 0.8)
    return belief1, belief2, belief3


# --8<-- [start:simulate]
def simulate(steps=15, seed=0, hallway=HALLWAY, p_correct=P_CORRECT, kernel=MOVE_KERNEL):
    """Run the robot for a number of sense-then-move steps; yield what happens."""
    rng = np.random.default_rng(seed)
    n = hallway.size
    true_cell = int(rng.integers(n))
    belief = np.full(n, 1.0 / n)  # "I could be anywhere"

    for step in range(steps):
        sees_truth = rng.random() < p_correct
        z = hallway[true_cell] if sees_truth else 1 - hallway[true_cell]
        belief = update(belief, hallway, z, p_correct)
        yield dict(step=step, true_cell=true_cell, z=int(z), belief=belief)

        true_cell = (true_cell + rng.choice(len(kernel), p=kernel)) % n
        belief = predict(belief, kernel)
# --8<-- [end:simulate]


BARS = " ▁▂▃▄▅▆▇█"


def bar_chart(belief):
    """One character per cell, scaled so the most likely cell is a full block."""
    levels = np.round(belief / belief.max() * (len(BARS) - 1)).astype(int)
    return " ".join(BARS[i] for i in levels)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=8)
    parser.add_argument("--steps", type=int, default=15)
    args = parser.parse_args()

    print("hallway   " + " ".join("D" if c == DOOR else "." for c in HALLWAY))
    for s in simulate(args.steps, args.seed):
        belief = s["belief"]
        best = int(np.argmax(belief))
        sensed = "door" if s["z"] == DOOR else "wall"
        print(f"\nstep {s['step']:2d}   sensed {sensed}; most likely cell {best} "
              f"with p = {belief[best]:.2f} (truly in cell {s['true_cell']})")
        print("belief    " + bar_chart(belief))
        print("robot     " + " ".join("^" if i == s["true_cell"] else " "
                                      for i in range(HALLWAY.size)))


if __name__ == "__main__":
    main()
