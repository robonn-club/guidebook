# 1 · Where am I? The Bayes filter

> A robot is switched on somewhere in a hallway. It has a map but does not know where it is.
> By the end of this lesson you will have written the ten lines of code that let it work out
> its position, and you will understand the idea behind almost every robot localization
> system.

!!! info "Lesson 1 of 4 · about 45 minutes"
    **You need:** basic Python. No probability background; it is introduced as you go.<br>
    **You will be able to:** represent what a robot believes as probabilities, update that
    belief from motion and sensor readings, and say how sure the robot should be.

---

## The problem

The hallway loops around and is divided into 20 cells. Some cells have a door. The robot has
a map of where the doors are, and two abilities:

- **Sense:** it looks at the wall beside it and reports *door* or *wall*. The sensor is right
  90 % of the time.
- **Move:** it drives one cell forward. Its wheels sometimes slip: it moves exactly one cell
  90 % of the time, stays put 5 % of the time, and overshoots to the second cell 5 % of the time.

It has just been switched on. Where is it?

## Try it

Press **Sense** and **Move** a few times. The bars show the robot's *belief*, the
probability that it is in each cell. Keep "Show where the robot really is" unchecked at first
and try to work it out from the bars alone.

<div class="bayes-demo"></div>

Things to notice:

- Before any reading, every bar has the same height: 5 %, "I could be anywhere."
- After **Sense**, cells that match the reading grow and the others shrink.
- **Move** shifts the bars one cell to the right and blurs them a little. Moving never makes
  the robot more sure of where it is.
- After a few rounds, one bar towers over the rest. The robot has localized itself.

## The idea: keep a belief, not a guess

The robot does not commit to one answer. It keeps a probability for **every** cell, a
list of 20 numbers that add up to 1. This list is the **belief**, written $bel(x)$, where $x$
is a cell.

Every step it runs the same two operations.

### Correct: what does the reading tell me?

When the sensor reports $z$ ("door"), ask of every cell: *if I were here, how likely would
I be to see this?* That number is the **likelihood** $p(z \mid x)$:

- a door cell explains "door" well: $p(\text{door} \mid \text{door cell}) = 0.9$
- a wall cell explains it badly: $p(\text{door} \mid \text{wall cell}) = 0.1$

Multiply each cell's belief by its likelihood, then rescale so everything adds up to 1 again:

$$
bel(x) = \eta \; p(z \mid x) \; \overline{bel}(x)
$$

Here $\overline{bel}(x)$ ("bel bar") is the belief *before* the reading, and $\eta$ is just
"one over the total," the number that makes the result sum to 1.

!!! note "This is Bayes' rule"
    $P(A \mid B) \propto P(B \mid A)\,P(A)$: what you believe after the evidence is
    proportional to how well each possibility explains the evidence, times what you believed
    before. [3Blue1Brown's visual explanation](https://www.youtube.com/watch?v=HZGCoVF3YvM)
    is the best 15 minutes you can spend on it.

### Predict: where could I be after moving?

When the robot moves one cell, cell $x$ can be reached from three places: from $x-1$ (moved
exactly one, probability 0.9), from $x$ (did not move, 0.05), or from $x-2$ (overshot, 0.05).
So the new belief in $x$ is a weighted sum:

$$
\overline{bel}(x) = 0.9\,bel(x-1) + 0.05\,bel(x) + 0.05\,bel(x-2)
$$

In general, with $p(x \mid u, x')$ the probability of ending in $x$ when starting in $x'$ and
executing motion $u$:

$$
\overline{bel}(x) = \sum_{x'} p(x \mid u, x') \; bel(x')
$$

!!! note "This is the law of total probability"
    To get the chance of ending up in $x$, add up every way of getting there, each weighted
    by how likely it was to start there.

That's the whole **Bayes filter**: *predict* with the motion model, *correct* with the
sensor model, repeat.

## Work it out by hand

Before reading the code, do one round on paper. Use a tiny five-cell hallway and a noisier
robot so the numbers stay friendly:

| cell | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| map | door | wall | door | wall | wall |

The sensor is right 80 % of the time. When told to move one cell, the robot moves one cell
80 % of the time, stays 10 %, overshoots 10 %. The robot starts with $bel = 0.2$ everywhere.

**Step 1: it senses "door".** Multiply by 0.8 for door cells and 0.2 for wall cells, then
normalize. Try it before opening the answer.

??? success "Answer"
    Unnormalized: $0.16,\ 0.04,\ 0.16,\ 0.04,\ 0.04$. They sum to $0.44$, so divide by it:

    | cell | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | $bel$ | 0.364 | 0.091 | 0.364 | 0.091 | 0.091 |

    The two door cells are now four times as likely as each wall cell.

**Step 2: it moves one cell.** Use $\overline{bel}(x) = 0.8\,bel(x-1) + 0.1\,bel(x) + 0.1\,bel(x-2)$,
remembering that the hallway loops (cell $-1$ is cell 4).

??? success "Answer"
    For example, cell 1: $0.8 \cdot 0.364 + 0.1 \cdot 0.091 + 0.1 \cdot 0.091 = 0.309$.

    | cell | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | $\overline{bel}$ | 0.118 | 0.309 | 0.145 | 0.309 | 0.118 |

    The peaks moved one cell right and got lower: the robot is less sure than before.

**Step 3: it senses "wall".** Multiply by 0.2 for door cells, 0.8 for wall cells, normalize.

??? success "Answer"

    | cell | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | $bel$ | 0.037 | 0.385 | 0.045 | 0.385 | 0.147 |

    The robot is almost certainly in cell 1 or cell 3, "just past a door." It cannot yet
    tell which, because both look the same from here. One more move and reading will
    usually settle it. This is a **multimodal** belief: two separate hypotheses, both kept
    alive until the evidence decides.

`bayes_filter_1d.py` reproduces these numbers in `worked_example()`, and the tests check
them.

## The code

The whole filter is two short functions. First the world:

```python title="examples/bayes_filter_1d.py"
--8<-- "bayes_filter_1d.py:world"
```

The correction step multiplies by the likelihood and normalizes:

```python
--8<-- "bayes_filter_1d.py:update"
```

The prediction step adds up the three ways of arriving in each cell. `np.roll` shifts the
whole array around the loop at once:

```python
--8<-- "bayes_filter_1d.py:predict"
```

The simulation hides a "true" robot from the filter and feeds it readings:

```python
--8<-- "bayes_filter_1d.py:simulate"
```

## Run it

```bash
python examples/bayes_filter_1d.py
```

Each step prints the belief as a row of bars (one per cell, tallest = most likely) and marks
the true robot with `^`. Here are some of the steps it prints:

```text
hallway   . . D D . D . D . . . . . D . D D D D .

step  0   sensed door; most likely cell 2 with p = 0.10 (truly in cell 14)
belief    ▁ ▁ █ █ ▁ █ ▁ █ ▁ ▁ ▁ ▁ ▁ █ ▁ █ █ █ █ ▁
robot                                 ^

step  3   sensed door; most likely cell 18 with p = 0.55 (truly in cell 17)
belief              ▁                     ▁ ▂ █ ▁
robot                                       ^

step 11   sensed door; most likely cell 5 with p = 0.97 (truly in cell 5)
belief              █
robot               ^

step 12   sensed door; most likely cell 6 with p = 0.46 (truly in cell 5)
belief              ▅ █ ▅
robot               ^

step 14   sensed door; most likely cell 7 with p = 0.85 (truly in cell 7)
belief                  █   ▁
robot                   ^
```

Step by step:

- **Step 0:** one "door" reading and all nine door cells are equally likely, about 10 %
  each. A single reading says little. And this one is actually *wrong*: the robot is at a
  wall (cell 14). The filter cannot know that, and it does not need to.
- **Steps 1–3:** three more "door" readings, and these are correct. Four "door" readings in a row are best
  explained by the long run of doors at cells 15–18, so the belief concentrates there. The
  wrong first reading cost the filter a little accuracy but did no lasting damage, because
  wall cells kept a small probability instead of being ruled out.
- **Step 11:** 97 % sure, and right.
- **Step 12:** the robot's wheels slipped (it stayed in cell 5) and it saw a door. Look at
  what the filter does. If the robot had moved as told it would be in cell 6, which is a wall. So either
  the sensor lied (cell 6), or the wheels slipped (cell 5, a door), or it overshot (cell 7,
  also a door). Starting from full certainty in cell 5, those three explanations get
  $0.9 \cdot 0.1 = 0.09$, $0.05 \cdot 0.9 = 0.045$ and $0.05 \cdot 0.9 = 0.045$, which is
  50 % / 25 % / 25 % after normalizing. The run shows 46 % / 26 % / 26 % because it was 97 %
  sure, not 100 %. The filter keeps all three explanations until the next reading.
- **Step 14:** back to 85 % in the right cell.

!!! tip "The filter is honest about its confidence"
    Over 400 runs of 15 steps, the robot's final confidence in its best guess averaged
    **68 %**, and the best guess was right **67 %** of the time. When a Bayes filter's
    models match reality, "70 % sure" really means right about 70 % of the time. A robot
    that knows how much it doesn't know can slow down, look again, or ask for help.

    Why not 100 %? Every move risks a slip, and a single reading is wrong 10 % of the time,
    so some uncertainty always remains. Set the slip to 0 % in the demo and the robot
    becomes certain.

## Common mistakes

| Mistake | What you will see |
|---|---|
| Forgetting to normalize in `update` | The numbers shrink every step and soon underflow to zero |
| Shifting the wrong way (`np.roll(belief, -k)`) | The belief drifts left while the robot drives right, and the filter never settles |
| Modelling the sensor as perfect (`p_correct = 1.0`) when it is not | One wrong reading sets the true cell to exactly 0 %, and no later evidence can bring it back |
| Treating the tallest bar as the answer | At step 0 the "most likely cell" is a 10 % guess. Always look at how tall the tallest bar is |

## Check yourself

??? question "1. Why can moving never make the robot more certain?"
    The predicted belief in each cell is a weighted *average* of beliefs in nearby cells
    (the weights add up to 1). An average is never larger than the largest thing being
    averaged, so the tallest bar can only stay the same or get shorter.

??? question "2. The robot starts knowing nothing and senses 'door'. Nine of the 20 cells are doors. How likely is each door cell now?"
    Each door cell gets $0.05 \times 0.9 = 0.045$, and each wall cell gets $0.05 \times 0.1 = 0.005$.
    The total is $9 \times 0.045 + 11 \times 0.005 = 0.46$, so each door cell has
    $0.045 / 0.46 \approx 9.8\%$ and each wall cell about $1.1\%$. That's the "about 10 %" at
    step 0 above.

??? question "3. What happens if the sensor is right only 50 % of the time?"
    Then $p(z \mid x) = 0.5$ for every cell, whatever the reading. Multiplying every cell by the
    same number and normalizing changes nothing. A sensor that is right half the time carries
    no information.

??? question "4. The robot keeps sensing without moving. Does its belief keep improving?"
    According to the model, yes: every reading is treated as fresh, independent evidence. In
    reality, a sensor that misreads a particular spot tends to keep misreading it (a strange
    reflection, say), so repeated readings from the same place are worth less than the model
    thinks. This independence is part of the *Markov assumption* behind the Bayes filter,
    and it is one reason real systems use cautious sensor models.

## Exercises

1. **In the demo:** set the sensor to 60 % and the slip to 20 %. How many steps does it take
   to reach 50 % confidence? Why?
2. **Change the map:** make a hallway with a single door. Run the script. Why does the robot
   stay unsure for a long time, then become sure all at once?
3. **Kidnap the robot:** in `simulate`, move `true_cell` to a random cell halfway through the
   run without telling the filter. Does the belief recover? What does it depend on?
   *(Hint: think about the smallest probability any cell can have.)*
4. **Two sensors:** add a second sensor that is right 70 % of the time and call `update` once
   for each reading. Compare how fast the robot localizes.

## Go deeper

- **Video:** [Bayes Filter in 5 minutes](https://www.youtube.com/watch?v=oUq0a8jHSQg) and the
  full [Bayes filter derivation](https://www.youtube.com/watch?v=0lKHFJpaZvE), both by Cyrill Stachniss (Universität Bonn).
- **Free book:** Roger Labbe, *Kalman and Bayesian Filters in Python*,
  [chapter 2: Discrete Bayes Filter](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/02-Discrete-Bayes.ipynb).
  It tracks a dog in a hallway with the same predict and correct steps, as an interactive notebook.
- **Textbook:** Thrun, Burgard & Fox, *Probabilistic Robotics* (MIT Press, 2005), Chapter 2
  *Recursive State Estimation* derives the Bayes filter formally, and Chapter 7 applies it to
  localization under the name *Markov localization*.

[Next: the Kalman filter :material-arrow-right:](2-kalman-filter.md){ .md-button .md-button--primary }
