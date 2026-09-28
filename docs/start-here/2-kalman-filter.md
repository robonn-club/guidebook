# 2 · From histograms to Gaussians: the Kalman filter

> Lesson 1 stored one probability per cell. That works for 20 cells but not for a real
> robot. In this lesson you replace the list of probabilities with just two numbers, and the
> Bayes filter turns into the Kalman filter, one of the most widely used estimators in engineering.

!!! info "Lesson 2 of 4 · about 45 minutes"
    **You need:** [Lesson 1](1-bayes-filter.md).<br>
    **You will be able to:** fuse a prediction with a measurement, explain the Kalman gain,
    and say when to trust a sensor and when to trust your own motion.

---

## The problem with cells

To localize a robot in a 100 m × 100 m field to 1 cm with Lesson 1's filter, you need
$10^4 \times 10^4 = 10^8$ cells. Add the heading in 1° steps and it is $3.6 \times 10^{10}$
numbers to update every step. Grids do not scale.

The fix is to assume the belief has a fixed *shape* and store only the numbers that describe
it. The standard choice is the **Gaussian** (the bell curve), described by two numbers:

- the **mean** $\mu$: the best guess, and
- the **variance** $\sigma^2$: how unsure you are. Its square root $\sigma$, the standard deviation, is in metres. About 95 % of
  the probability lies within $\mu \pm 2\sigma$.

## The scenario

A lawn-mower robot drives along a straight 100 m row. Every second it is told to drive 1 m
forward, but its wheels slip on the grass: the actual distance has a standard deviation of
0.2 m. A cheap GPS receiver reports its position with a standard deviation of 2 m.

- **Odometry alone** is precise over one step but the errors add up. After 100 steps the
  standard deviation is $0.2\,\sqrt{100} = 2$ m, and it keeps growing.
- **GPS alone** never drifts, but every single reading may be off by several metres.

Can we do better than both?

## Predict: variances add

The robot believes it is at $\mu$ with variance $\sigma^2$. It drives $u$ metres, with
slip variance $\sigma_u^2$. Its new belief:

$$
\bar\mu = \mu + u, \qquad \bar\sigma^2 = \sigma^2 + \sigma_u^2
$$

The mean moves. The variances *add*, because independent uncertainties add up. This is Lesson 1's
"shift and blur," with the blur now a single number.

## Correct: fuse two Gaussians

The GPS reports $z$ with variance $\sigma_z^2$. Lesson 1 said: multiply the belief by the
likelihood and normalize. Multiplying two Gaussians gives another Gaussian, and its mean and
variance have a clean form:

$$
K = \frac{\bar\sigma^2}{\bar\sigma^2 + \sigma_z^2}, \qquad
\mu = \bar\mu + K\,(z - \bar\mu), \qquad
\sigma^2 = (1 - K)\,\bar\sigma^2
$$

$K$ is the **Kalman gain**, a number between 0 and 1 that says how far to move toward the
measurement:

- The GPS is much better than your prediction ($\sigma_z \ll \bar\sigma$): $K \approx 1$,
  jump to the measurement.
- Your prediction is much better ($\bar\sigma \ll \sigma_z$): $K \approx 0$, barely move.
- Equally good: $K = 0.5$, go halfway.

$z - \bar\mu$ is called the **innovation**, the part of the measurement you did not expect.

??? note "Where do these formulas come from?"
    Bayes' rule says $bel(x) \propto p(z \mid x)\,\overline{bel}(x)$. Both factors are
    Gaussians in $x$, so the product is proportional to

    $$
    \exp\!\left(-\frac{(x - \bar\mu)^2}{2\bar\sigma^2} - \frac{(z - x)^2}{2\sigma_z^2}\right).
    $$

    The exponent is a quadratic in $x$. Completing the square gives a Gaussian with

    $$
    \frac{1}{\sigma^2} = \frac{1}{\bar\sigma^2} + \frac{1}{\sigma_z^2}, \qquad
    \mu = \sigma^2 \left(\frac{\bar\mu}{\bar\sigma^2} + \frac{z}{\sigma_z^2}\right),
    $$

    which is the same as the $K$ form above after some algebra. The left-hand formula is
    worth remembering: **information adds**. $1/\sigma^2$ measures how much you know, and
    fusing adds what the prediction knows to what the measurement knows. So the result is
    always more certain than either input.

## Try it

Drag the sliders. The shaded curve is the fused belief.

<div class="gauss-demo"></div>

Things to try:

- Make the GPS very noisy. The fused curve sits on top of the prediction.
- Make the prediction and the GPS equally uncertain. The result lands exactly halfway.
- Put the measurement far from the prediction. The result still lands between them, and it is
  still *narrower* than both. A Kalman filter becomes more certain even when its two sources
  disagree. Keep that in mind: when a sensor fails badly, a plain Kalman filter will trust
  the wrong answer confidently.

## Work it out by hand

The robot believes it is at 10.0 m with $\sigma = 0.3$ m. It drives 1 m (slip
$\sigma_u = 0.4$ m), then the GPS says 12.0 m ($\sigma_z = 1.0$ m). Compute the new belief.

??? success "Answer"
    **Predict:** $\bar\mu = 10.0 + 1.0 = 11.0$ m, and $\bar\sigma^2 = 0.3^2 + 0.4^2 = 0.09 + 0.16 = 0.25$,
    so $\bar\sigma = 0.5$ m.

    **Gain:** $K = 0.25 / (0.25 + 1.0) = 0.2$.

    **Correct:** $\mu = 11.0 + 0.2 \times (12.0 - 11.0) = 11.2$ m, and
    $\sigma^2 = (1 - 0.2) \times 0.25 = 0.2$, so $\sigma \approx 0.45$ m.

    The GPS pulled the estimate only a fifth of the way, because the prediction was four times
    more certain (variance 0.25 against 1.0). Check with the information form:
    $1/0.25 + 1/1 = 5 = 1/0.2$. ✓

## The code

The entire filter:

```python title="examples/kalman_filter_1d.py"
--8<-- "kalman_filter_1d.py:kf"
```

The simulation drives a hidden true robot and runs three estimators side by side:

```python
--8<-- "kalman_filter_1d.py:simulate"
```

## Run it

```bash
python examples/kalman_filter_1d.py
```

```text
One 100 m run            error (RMSE)
  odometry only           1.70 m
  GPS only                1.95 m
  Kalman filter           0.59 m
  filter's own std at the end: 0.62 m (steady state 0.62 m)
```

The Kalman filter is about three times more accurate than either source on its own. Over 300 runs the
average errors were 1.33 m (odometry), 1.99 m (GPS) and 0.59 m (Kalman filter), and the
filter beat odometry in 92 % of runs.

![Estimation error of odometry, GPS and the Kalman filter over 100 steps](assets/kf_run-light.svg#only-light)
![Estimation error of odometry, GPS and the Kalman filter over 100 steps](assets/kf_run-dark.svg#only-dark)

Read the plot:

- **GPS** (dots) scatters by several metres at every step but does not drift.
- **Odometry** (dashed) is smooth but wanders off, and nothing pulls it back.
- **The Kalman filter** (solid) is smooth *and* stays close to the truth. The shaded band is
  the filter's own ±2σ. The true error stays inside it about 95 % of the time (95.9 % over
  300 runs), which means the filter is honest about its uncertainty.
- **The band stops shrinking.** Each step adds 0.2 m of slip and each GPS reading takes
  some uncertainty away. They balance at $\sigma \approx 0.62$ m, the *steady state*.

## It really is the same filter

`kalman_filter_1d.py` also runs Lesson 1's histogram filter on a grid of 1 cm cells, with
Gaussian motion blur and a Gaussian GPS likelihood, over the first 10 GPS readings:

```text
  Kalman filter:  mean 9.5230 m, variance 0.35993 m^2
  histogram:      mean 9.5230 m, variance 0.35993 m^2
```

Five thousand cells and two numbers give the same answer. When motion and sensing are
*linear* with Gaussian noise, the belief stays exactly Gaussian, and the Kalman filter is the
Bayes filter with no approximation at all.

## From one dimension to many

A real state has several numbers (position, velocity, heading and so on). The mean becomes a vector
$\mu$, the variance becomes a **covariance matrix** $\Sigma$, and each scalar operation has a
matrix counterpart. In the notation of *Probabilistic Robotics*, where the state moves as
$x_t = A x_{t-1} + B u_t + \varepsilon$ with noise covariance $R$, and is measured as
$z_t = C x_t + \delta$ with noise covariance $Q$:

| | 1D (this lesson) | Many dimensions |
|---|---|---|
| Predict mean | $\bar\mu = \mu + u$ | $\bar\mu = A\mu + Bu$ |
| Predict uncertainty | $\bar\sigma^2 = \sigma^2 + \sigma_u^2$ | $\bar\Sigma = A\Sigma A^\top + R$ |
| Kalman gain | $K = \bar\sigma^2 / (\bar\sigma^2 + \sigma_z^2)$ | $K = \bar\Sigma C^\top (C\bar\Sigma C^\top + Q)^{-1}$ |
| Correct mean | $\mu = \bar\mu + K(z - \bar\mu)$ | $\mu = \bar\mu + K(z - C\bar\mu)$ |
| Correct uncertainty | $\sigma^2 = (1 - K)\,\bar\sigma^2$ | $\Sigma = (I - KC)\,\bar\Sigma$ |

Read each row side by side and you will see the same idea. This all requires $A$ and $C$ to
be *linear*, and a real robot that turns is not linear. That is the next lesson.

## Common mistakes

| Mistake | What you will see |
|---|---|
| Using standard deviations instead of variances in $K$ | $K = 0.5/(0.5+1) = 0.33$ instead of $0.2$ in the example above: the filter over-trusts the noisier source |
| Forgetting to add the motion noise in `predict` | The variance shrinks with every GPS reading and never grows back. The filter grows ever more confident, pays less and less attention to the GPS, and drifts off with the odometry |
| Telling the filter the GPS is better than it is | The estimate jitters with every reading, and the true error often leaves the ±2σ band |
| Telling the filter the GPS is worse than it is | The estimate is smooth but follows the odometry too closely, so it drifts further from the truth |

## Check yourself

??? question "1. The prediction and the measurement have the same variance. What is K, and where does the estimate land?"
    $K = \bar\sigma^2 / (2\bar\sigma^2) = 0.5$, exactly halfway between them. Its variance is
    half of either input.

??? question "2. The GPS stops working for 20 steps. What happens to the belief?"
    Only `predict` runs. The mean follows odometry and the variance grows by $0.2^2 = 0.04$ m²
    every step: from about $0.38$ m² to $1.18$ m², so $\sigma$ goes from 0.62 m to about 1.09 m.
    When the GPS returns, $K$ is large and the filter quickly pulls back toward it.

??? question "3. Why is the fused estimate more certain than both inputs, even when they disagree?"
    Because $1/\sigma^2 = 1/\bar\sigma^2 + 1/\sigma_z^2$: the information from both sources
    adds up, whatever the actual values of $\bar\mu$ and $z$. The Kalman filter's variance
    does not depend on the measurements at all. That is efficient when the models are right,
    and dangerous when a sensor is broken, which is why real systems check the innovation
    before trusting a reading.

## Exercises

1. **GPS outage:** in `simulate`, skip the `update` for steps 40–60. Print `sqrt(var)` over
   time and compare it with your answer to question 2.
2. **A wrong model:** keep the real GPS noise at 2 m but pass `meas_var=0.5**2` to
   `update`. How do the error and the fraction of steps inside ±2σ change?
3. **A robot that accelerates:** track position *and* velocity, with
   $A = \begin{bmatrix}1 & \Delta t\\ 0 & 1\end{bmatrix}$ and $C = [1\ \ 0]$ (GPS measures
   position only). Use the matrix column of the table above. The velocity estimate appears
   even though nothing measures velocity directly.

## Go deeper

- **Video:** [Kalman Filter in 5 minutes](https://www.youtube.com/watch?v=o_HW6GnLqvg), Cyrill Stachniss.
- **Free book:** Roger Labbe, [*Kalman and Bayesian Filters in Python*](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python).
  Its chapters on Gaussians, the one-dimensional Kalman filter and the multivariate Kalman filter
  build this lesson out step by step, with interactive notebooks.
- **Tutorial:** G. Welch and G. Bishop, [*An Introduction to the Kalman Filter*](https://www.cs.utexas.edu/~pstone/Courses/393Rfall15/readings/Welch+Bishop-TR-95.pdf),
  UNC-Chapel Hill TR 95-041. A short classic with the matrix equations and a worked example.
- **Textbook:** Thrun, Burgard & Fox, *Probabilistic Robotics*, Chapter 3 *Gaussian Filters*.
  The notation in this guidebook follows it.
- **The original:** R. E. Kalman, "A New Approach to Linear Filtering and Prediction Problems,"
  *Journal of Basic Engineering* 82(1), 1960, [doi:10.1115/1.3662552](https://doi.org/10.1115/1.3662552).

[Next: localizing a real robot :material-arrow-right:](3-ekf-localization.md){ .md-button .md-button--primary }
