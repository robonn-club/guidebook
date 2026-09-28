# 4 · When one Gaussian is not enough: the particle filter

> The EKF needed a good starting guess and landmarks with labels. Take both away. The robot
> wakes up somewhere in the arena, facing any direction, and every pole looks the same.
> In this lesson you represent the belief with thousands of guesses instead of one Gaussian,
> and the robot finds itself within a few seconds.

!!! info "Lesson 4 of 4 · about 60 minutes"
    **You need:** [Lesson 3](3-ekf-localization.md) (the same robot, motion model and sensor
    model).<br>
    **You will be able to:** implement Monte Carlo localization, explain resampling and
    particle deprivation, and choose between an EKF and a particle filter.

---

## What the robot knows after one reading

Suppose the robot sees one pole, 4 m away and directly to its right. Where could it be?

With labelled poles it would be somewhere on a circle around *that* pole. Without labels, it
is on a circle around **any** of the six poles. Its belief is six rings, and no Gaussian
comes close to that shape.

![Four snapshots: particles uniformly spread, then arranged on rings around every pole after one reading, then a single cluster at the true position](assets/pf_snapshots-light.svg#only-light)
![Four snapshots: particles uniformly spread, then arranged on rings around every pole after one reading, then a single cluster at the true position](assets/pf_snapshots-dark.svg#only-dark)

From left to right: before any reading, after one reading, after the first full scan (three
poles in view), and 5 s later. The first three panels use 200,000 particles so the rings are
easy to see. The filter itself uses 5,000.

The rings disappear as soon as the robot sees three poles at once. Only a few places in the
arena have three poles arranged like that around them, and the poles were placed
deliberately *without* symmetry. If the layout looked the same from two places, no amount
of looking could tell them apart. The correct belief would then have two clusters forever,
and Exercise 2 shows what a particle filter actually does in that case.

## The idea: many guesses

A **particle** is one complete guess of the robot's pose $(x, y, \theta)$. The belief is a
cloud of many particles: where they are dense, the robot is likely to be. The Bayes filter
steps from Lesson 1 become operations on the cloud:

1. **Predict:** move every particle with the odometry, each with its *own* random draw of
   the motion noise. The cloud drifts and spreads, just like Lesson 1's shift-and-blur.
2. **Weight:** give each particle a weight $w = p(z \mid \text{particle})$, how well it
   explains the reading. This is Lesson 1's correction step.
3. **Resample:** draw a new cloud from the old one, picking particles in proportion to their
   weight. Heavy particles are copied, light ones disappear. The cloud now concentrates where
   the evidence points.

That's the whole particle filter. In robot localization it is called
**Monte Carlo localization (MCL)**. The default localization in the ROS 2 navigation stack
(Nav2's `amcl`) is an adaptive version of it.

## The code

**Start anywhere.** The initial cloud covers the whole arena with random headings:

```python title="examples/particle_filter.py"
--8<-- "particle_filter.py:init"
```

**Predict.** This is Lesson 3's motion model applied to all 5,000 particles at once:

```python
--8<-- "particle_filter.py:predict"
```

**Weight.** For a labelled pole, the likelihood is Lesson 3's Gaussian around the expected
reading. Without labels the reading could come from any of the $J$ poles, so the likelihood
averages over them:

$$
p(z \mid x) = \frac{1}{J} \sum_{j=1}^{J} p(z \mid x, \text{pole } j)
$$

```python
--8<-- "particle_filter.py:weight"
```

Weights are handled as logarithms. A product of a few Gaussian likelihoods can easily be
$10^{-300}$, which a 64-bit float rounds to zero. Adding logs and subtracting the largest value
before `exp` avoids that. It is the same trick as `log-sum-exp` in machine learning.

**Resample.** The *low-variance* resampler uses a single random number and evenly spaced
pointers, so a particle with weight $w$ is copied either $\lfloor nw \rfloor$ or
$\lceil nw \rceil$ times. That keeps more diversity than $n$ independent draws:

```python
--8<-- "particle_filter.py:resample"
```

The loop resamples only when the **effective sample size** drops below half the particle
count. When the weights are nearly even there is nothing to gain from resampling, and every
resampling throws some diversity away.

## Run it

```bash
python examples/particle_filter.py
```

```text
Global localization with 5,000 particles, unlabelled poles
   time   position error   particle spread
    0.0 s         0.65 m         0.07 m
    0.5 s         0.53 m         0.10 m
    1.0 s         0.45 m         0.12 m
    2.0 s         0.20 m         0.13 m
    5.0 s         0.11 m         0.11 m
   10.0 s         0.09 m         0.09 m
   20.0 s         0.04 m         0.13 m
   39.9 s         0.04 m         0.09 m
```

After the first scan the robot is within 65 cm, from a starting point of "anywhere in
an 800 m² arena," and within about 10 cm after 5 s.

Compare the two columns. For the first second the cloud's *spread* (7–12 cm) is much smaller
than its *error* (45–65 cm), so the filter is more confident than it should be. With only 5,000
guesses spread over the whole arena, none landed very close to the truth, and the best few
took over. It recovers because the particles keep moving with random noise, and by 5 s
spread and error agree. The next section shows what happens when it does not recover.

## Particle filter vs. EKF

Same runs, same unlabelled poles. The EKF has to guess which pole each reading belongs to,
and it picks the pole closest to its prediction (*nearest-neighbour* association). Over 20
runs, the number of runs that ended within 0.5 m of the truth:

| Filter | Runs that localize |
|---|---|
| EKF, started at the true pose | 20 / 20 |
| EKF, started from a random guess | 7 / 20 |
| Particle filter, 5,000 particles, no initial guess at all | 20 / 20 |

From a good start the EKF tracks perfectly; it's precise and cheap. From a bad start, it
assigns readings to the wrong poles and converges confidently to the wrong place. The
particle filter never has to commit to one hypothesis, so it does not care where it
starts. Run `python examples/particle_filter.py --compare` to reproduce these numbers (it takes about a minute).

## Particle deprivation and roughening

The particle filter only works if some particles are near the truth. When a sharp
measurement gives almost all the weight to a handful of particles, resampling fills the whole
cloud with copies of them. If those few were slightly off, the copies are too, and there
is nothing left near the truth to recover with. This is called **particle deprivation**.

A simple defence is **roughening**: after resampling, nudge every particle by a little random
noise (here 5 cm and 1°) so that copies spread out and explore their neighbourhood. From the
same `--compare` run:

| Particles | Runs that localize without roughening | with roughening |
|---|---|---|
| 200 | 6 / 20 | 16 / 20 |
| 500 | 12 / 20 | 18 / 20 |
| 1,000 | 19 / 20 | 19 / 20 |
| 5,000 | 20 / 20 | 20 / 20 |

With plenty of particles it makes no difference. With few, it is the difference between
working and not. More particles is the other fix, but the cost grows with them.

```python
--8<-- "particle_filter.py:roughen"
```

## The price

The EKF updates a 3-number mean and a 3 × 3 covariance. The particle filter evaluates the sensor
model for every particle, for every pole, for every reading: here 5,000 × 6 likelihoods per
reading. For a 3-dimensional state that is fine on any laptop. But the number of particles
needed to cover a space grows roughly *exponentially* with its number of dimensions, so a
plain particle filter over a robot pose *and* a map with hundreds of landmarks is hopeless.
SLAM systems such as FastSLAM combine the two ideas instead: particles for the pose, and small
Kalman filters for each landmark. See [SLAM](../courses/7_slam/README.md).

**Rule of thumb:** use an EKF when you have a reasonable initial guess and the belief stays
one blob. Use a particle filter when the belief can split into several hypotheses: global
localization, look-alike landmarks, symmetric environments, recovery after the robot has
been picked up and moved.

## Common mistakes

| Mistake | What you will see |
|---|---|
| Multiplying raw likelihoods instead of adding logs | All weights become 0, then `nan` after normalizing |
| Resampling every step, even without a new reading | The cloud loses diversity for no gain, because resampling adds randomness without adding information |
| Reporting the weighted mean of a multimodal cloud | With two clusters, the "estimate" lies between them, where the robot certainly is not |
| Using the same noise sample for every particle in `predict` | The whole cloud moves rigidly and never spreads |
| Too few particles, no roughening | The filter converges confidently to the wrong place (see the table above) |

## Check yourself

??? question "1. After one reading of an unlabelled pole, why are there six rings and not one?"
    The reading says "a pole is 4 m away," but not which pole. Each of the six poles is an
    equally good explanation, so the belief is the union of a ring around each. The bearing
    ties each position on a ring to a particular heading (the one that puts the pole to the
    robot's right), so in $(x, y, \theta)$ space each ring is a helix.

??? question "2. Resampling does not use the measurement. Why does it help at all?"
    It does not add information. The weights already contain it. Resampling moves the
    particles to where the weights are high, so the *next* prediction and weighting spend
    their effort on plausible poses rather than on the thousands of particles that have
    already been ruled out.

??? question "3. The filter has converged, then someone carries the robot to the other side of the arena. What happens?"
    Every particle is near the old position, so none can explain the new readings. The
    weights are all tiny, but after normalizing they still sum to 1, and the filter stays
    wrong. The standard fix is to keep injecting a few random particles across the whole
    map, more when the measurements fit badly. *Probabilistic Robotics* calls this
    *augmented MCL* (Chapter 8).

## Exercises

1. **Kidnap the robot.** In `robot_run`, teleport `x_true` to another place at step 200.
   Confirm that the filter does not recover. Then add random particles: after each
   resampling, replace 1 % of the particles with fresh `uniform_particles`. Does it recover
   now? What does this cost while the robot is *not* kidnapped?
2. **A symmetric world.** In `ekf_localization.py`, move the pole at (5, 21) to (9, 17), which
   makes the layout look the same after a half-turn around (0, 10). The robot's position and
   its mirror image across (0, 10) now explain every reading equally well, so the correct belief has two clusters
   forever. Run a few seeds and look at the particles every few seconds. Does the filter keep
   both?
3. **A short-sighted sensor.** Reduce `MAX_RANGE` to 8 m so that the robot usually sees only one
   or two poles. How many particles do you need now for 20 / 20 runs?

??? tip "What we saw in Exercise 2"
    No. In each of three runs, within 10 s all the weight sat in a single cluster, and in
    one of the three it was the *wrong* one: a confident estimate on the far side of the
    arena. Each resampling copies particles at random, and two equally good clusters
    drift apart in size until one dies out. This is sample impoverishment again, and a
    reminder that a particle filter only *approximates* the Bayes filter. Remedies include
    more particles, resampling less often, and methods that track each cluster
    separately.

## Go deeper

- **Video:** [Particle Filter and Monte Carlo Localization](https://www.youtube.com/watch?v=MsYlueVDLI0)
  (full lecture) and [Particle Filter in 5 minutes](https://www.youtube.com/watch?v=YBeVDxTHiYM), Cyrill Stachniss.
- **Textbook:** Thrun, Burgard & Fox, *Probabilistic Robotics*: Chapter 4 *Nonparametric
  Filters* (the particle filter and low-variance resampling) and Chapter 8 *Mobile Robot
  Localization: Grid and Monte Carlo* (MCL and recovering from kidnapping).
- **The MCL paper:** F. Dellaert, D. Fox, W. Burgard and S. Thrun,
  [Monte Carlo Localization for Mobile Robots](https://www.ri.cmu.edu/pub_files/pub1/dellaert_frank_1999_2/dellaert_frank_1999_2.pdf),
  ICRA 1999. Followed by S. Thrun, D. Fox, W. Burgard and F. Dellaert,
  [Robust Monte Carlo localization for mobile robots](https://www.sciencedirect.com/science/article/pii/S0004370201000698),
  *Artificial Intelligence*, 2001.
- **Where particle filters come from:** N. J. Gordon, D. J. Salmond and A. F. M. Smith, "Novel approach
  to nonlinear/non-Gaussian Bayesian state estimation," *IEE Proceedings F* 140(2), 1993,
  [doi:10.1049/ip-f-2.1993.0015](https://doi.org/10.1049/ip-f-2.1993.0015). This paper introduced
  the bootstrap filter, and roughening along with it.
- **A deeper tutorial:** A. Doucet and A. M. Johansen,
  [A Tutorial on Particle Filtering and Smoothing: Fifteen years later](https://www.stats.ox.ac.uk/~doucet/doucet_johansen_tutorialPF2011.pdf),
  including the effective-sample-size criterion used here.

---

## You finished the path

You have built the three filters behind most robot localization, and you know how to test
them. Where to go from here is on the [Start Here](index.md#after-the-path) page.
