# 3 · Localizing a real robot: the Extended Kalman Filter

> A wheeled robot drives around an arena with a few poles at known positions. It measures
> the distance and direction to the poles it can see. In this lesson you build the filter
> that tracks its position *and* heading to within about 10 cm, and learn how to tell
> whether such a filter is working.

!!! info "Lesson 3 of 4 · about 90 minutes"
    **You need:** [Lesson 2](2-kalman-filter.md); matrix multiplication; what a derivative is.<br>
    **You will be able to:** linearize a motion and a sensor model, run an EKF, and test it
    with Jacobian checks and consistency statistics.

---

## The robot

The robot's state is its pose $x = (x, y, \theta)$: position in metres and heading in
radians. Each 0.1 s:

- **It moves.** Wheel odometry reports a forward speed $v$ and a turn rate $\omega$, with noise:
  standard deviation 0.1 m/s on $v$ and 0.05 rad/s on $\omega$.
- **It looks around.** Every 0.5 s a sensor reports the **range** $r$ (distance) and
  **bearing** $\phi$ (angle relative to the robot's heading) to each pole within 12 m. Noise:
  0.2 m and 3°.

For this lesson we also assume two conveniences, which Lesson 4 removes:

1. The robot knows *which* pole each reading comes from (as if each pole had a unique label).
2. It starts with a good guess of where it is.

## Why the Kalman filter is not enough

The Kalman filter assumed motion and sensing are *linear*. For this robot they are not.
Driving forward moves it by $v\,\Delta t\cos\theta$ along $x$, and bearing involves an
$\arctan$. Push a Gaussian through a nonlinear function and what comes out is not Gaussian:

![A pose with uncertain heading driven 4 m forward ends up on a curved arc, while the EKF predicts a thin ellipse](assets/ekf_linearization-light.svg#only-light)
![A pose with uncertain heading driven 4 m forward ends up on a curved arc, while the EKF predicts a thin ellipse](assets/ekf_linearization-dark.svg#only-dark)

The robot starts at the origin knowing its position well but its heading only to ±25°, then
drives 4 m. The true set of possible end positions (grey) is a **banana-shaped arc**. The
EKF's Gaussian (blue) is a thin vertical ellipse centred at exactly 4 m. It gets the sideways
spread roughly right (about 10 % too wide) but misses the curve, and its mean is ahead of
the true mean.

This is the price of the EKF. It is a good approximation when the uncertainty is small
compared with how curved the functions are, and a poor one when it is not. With odometry
at 10 Hz and poles in view, this robot's uncertainty stays small, and the EKF works very
well.

## The EKF idea: use the tangent

At the current best estimate, replace each nonlinear function by its **tangent** (its
first-order Taylor expansion), then run the ordinary Kalman filter equations. In more than
one dimension the "slope" is a matrix of partial derivatives called the **Jacobian**:

$$
g(x) \approx g(\mu) + G\,(x - \mu), \qquad G = \left.\frac{\partial g}{\partial x}\right|_{x=\mu}
$$

The matrices $A$ and $C$ from Lesson 2 become Jacobians $G$ and $H$, recomputed at every step
at the current estimate.

!!! warning "Notation: R and Q swap between books"
    This guidebook follows *Probabilistic Robotics*: **$R$ is the motion noise and $Q$ is the
    measurement noise.** Many other texts, including Wikipedia and Welch & Bishop, use the
    opposite. When you read code or papers, check which is which before copying numbers.

## The motion model and its Jacobians

One Euler step of a unicycle-type robot:

$$
g(x, u) = \begin{bmatrix} x + v\,\Delta t\cos\theta \\ y + v\,\Delta t\sin\theta \\ \theta + \omega\,\Delta t \end{bmatrix}
$$

Differentiate each row with respect to each state variable to get $G$, and with respect to each
control to get $V$:

$$
G = \frac{\partial g}{\partial (x, y, \theta)} =
\begin{bmatrix} 1 & 0 & -v\,\Delta t\sin\theta \\ 0 & 1 & v\,\Delta t\cos\theta \\ 0 & 0 & 1 \end{bmatrix},
\qquad
V = \frac{\partial g}{\partial (v, \omega)} =
\begin{bmatrix} \Delta t\cos\theta & 0 \\ \Delta t\sin\theta & 0 \\ 0 & \Delta t \end{bmatrix}
$$

The third column of $G$ says that **heading errors turn into position errors**, more so the
faster you drive.

The noise is known for $v$ and $\omega$ (covariance $M$), but the filter needs it in terms of
$x, y, \theta$. $V$ converts it: $R = V M V^\top$. This step is easy to miss, and it is why a
robot driving straight becomes uncertain *sideways*.

```python title="examples/ekf_localization.py"
--8<-- "ekf_localization.py:motion"
```

!!! note "Other motion models"
    *Probabilistic Robotics* (Chapter 5) derives an exact "velocity motion model" that moves
    along circular arcs, and an "odometry motion model." The Euler step used here is simpler
    and accurate for short time steps. The EKF recipe is the same whichever model you choose:
    write $g$, differentiate it.

## The sensor model and its Jacobian

For a pole at $(m_x, m_y)$, with $\Delta x = m_x - x$, $\Delta y = m_y - y$ and
$q = \Delta x^2 + \Delta y^2$:

$$
h(x) = \begin{bmatrix} r \\ \phi \end{bmatrix} =
\begin{bmatrix} \sqrt{q} \\ \operatorname{atan2}(\Delta y, \Delta x) - \theta \end{bmatrix},
\qquad
H = \begin{bmatrix}
-\Delta x/\sqrt{q} & -\Delta y/\sqrt{q} & 0 \\
\Delta y/q & -\Delta x/q & -1
\end{bmatrix}
$$

The $-1$ in the corner says that turning the robot left by some angle makes every pole appear
that much further to the right. The zero next to it says that turning does not change the
distance.

```python
--8<-- "ekf_localization.py:measurement"
```

## The filter

The Kalman filter from Lesson 2, with Jacobians in place of $A$ and $C$:

```python
--8<-- "ekf_localization.py:predict"
```

```python
--8<-- "ekf_localization.py:update"
```

Four details that matter:

- **Wrap the bearing innovation.** The sensor reads 179°, you expect −179°. The difference
  is 2°, not 358°. Without `wrap_angle` the filter makes a huge wrong correction.
- **Linearize at the right place.** `G` at the estimate *before* moving, `H` at the
  *predicted* estimate.
- **`np.linalg.solve` instead of `inv`.** Solving a linear system is more accurate and cheaper
  than forming an inverse.
- **The Joseph form** `(I - KH) Σ (I - KH)ᵀ + K Q Kᵀ` computes the same covariance as
  $(I - KH)\bar\Sigma$ but stays symmetric and positive definite when rounding errors pile up.

## Work it out by hand

Doing one step on paper is the best way to demystify the EKF. Take an easy starting point:

- belief $\mu = (0, 0, 0)$, $\Sigma = \operatorname{diag}(0.04,\ 0.04,\ 0.01)$ (σ of 0.2 m, 0.2 m, 0.1 rad)
- odometry $v = 1$ m/s, $\omega = 0$, $\Delta t = 1$ s, $M = \operatorname{diag}(0.01,\ 0.0025)$

**Predict.** Compute $\bar\mu$, $G$, $V$, $R$ and $\bar\Sigma$.

??? success "Answer"
    With $\theta = 0$: $\bar\mu = (1, 0, 0)$,

    $$
    G = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{bmatrix},\quad
    V = \begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix},\quad
    R = V M V^\top = \operatorname{diag}(0.01,\ 0,\ 0.0025),
    $$

    $$
    \bar\Sigma = G\Sigma G^\top + R =
    \begin{bmatrix} 0.05 & 0 & 0 \\ 0 & 0.05 & 0.01 \\ 0 & 0.01 & 0.0125 \end{bmatrix}.
    $$

    Look at the $y$ entries. The robot drove straight along $x$, yet its $y$ variance grew from
    0.04 to 0.05, and $y$ and $\theta$ are now **correlated** (0.01). A heading error of
    0.1 rad over 1 m of driving is 0.1 m sideways. The positive correlation says "if my
    heading is off to the left, I have also drifted left." That coupling is exactly what
    the next measurement will exploit.

**Update.** A pole at $(5, 3)$ is measured at $z = (4.8\text{ m},\ 0.70\text{ rad})$ with
$Q = \operatorname{diag}(0.01,\ 0.0025)$. Compute the expected measurement $\hat z$, $H$, and the
innovation $\nu = z - \hat z$. (Leave the 2 × 2 inverse to NumPy.)

??? success "Answer"
    From $\bar\mu = (1, 0, 0)$: $\Delta x = 4$, $\Delta y = 3$, so $r = 5$ and
    $\phi = \operatorname{atan2}(3, 4) = 0.6435$ rad (36.9°). So $\hat z = (5,\ 0.6435)$ and

    $$
    H = \begin{bmatrix} -0.8 & -0.6 & 0 \\ 0.12 & -0.16 & -1 \end{bmatrix}, \qquad
    \nu = (-0.2,\ 0.0565).
    $$

    Carrying on (this is what `worked_example()` in the code prints):

    $$
    S = H\bar\Sigma H^\top + Q = \begin{bmatrix} 0.06 & 0.006 \\ 0.006 & 0.0202 \end{bmatrix},\quad
    K = \bar\Sigma H^\top S^{-1} = \begin{bmatrix} -0.718 & 0.510 \\ -0.424 & -0.765 \\ -0.031 & -0.689 \end{bmatrix}
    $$

    $$
    \mu = \bar\mu + K\nu = (1.172,\ 0.042,\ -0.033), \qquad
    \sigma_x, \sigma_y, \sigma_\theta:\ (0.22, 0.22, 0.11) \rightarrow (0.14, 0.15, 0.05)
    $$

    Read it like a story. The pole is 0.2 m **closer** than expected, so the robot moves toward
    it (+0.17 m in $x$). The pole appears 3.2° **further left** than expected, and the last
    row of $K$ explains most of that as a heading error: the robot is turned 1.9° clockwise
    ($\theta = -0.033$ rad). One reading of one pole improved all three numbers, including
    heading, which nothing measures directly.

## Run it

```bash
python examples/ekf_localization.py
```

It first prints the worked example above, then drives one lap of a 10 m circle:

```text
One lap of simulation
  position RMSE, dead reckoning: 2.75 m
  position RMSE, EKF:            0.08 m
  mean NEES (expect about 3):    2.92
  mean NIS  (expect about 2):    2.13
```

![One lap: the dead-reckoning path drifts off the circle while the EKF estimate stays on the true path](assets/ekf_trajectory-light.svg#only-light)
![One lap: the dead-reckoning path drifts off the circle while the EKF estimate stays on the true path](assets/ekf_trajectory-dark.svg#only-dark)

Dead reckoning, which only integrates odometry, ends the lap 2.5 m from the truth. The
EKF stays within about 8 cm (RMSE) all the way round. Over 40 different runs, the EKF's
average position error was 9 cm and dead reckoning's was 1.7 m.

## Is my filter working?

A filter can produce plausible-looking tracks and still be wrong. Two checks catch most
bugs.

### 1. Check every Jacobian numerically

Hand-derived Jacobians are the most common source of EKF bugs. Compare each one with finite
differences, $\big(g(x + \varepsilon) - g(x - \varepsilon)\big) / 2\varepsilon$:

```python
--8<-- "ekf_localization.py:numerical_jacobian"
```

```python
G, V = motion_jacobians(x, u, dt)
G_check = numerical_jacobian(lambda s: motion_model(s, u, dt), x, angle_rows=[2])
assert np.allclose(G, G_check, atol=1e-6)
```

The guidebook's tests do exactly this for $G$, $V$ and $H$, at headings that include ±π.

### 2. Check that the filter is honest about its uncertainty

The filter's covariance claims how large its errors are. In simulation you know the truth,
so you can check the claim:

![Estimation errors in x, y and heading stay inside the filter's own ±2σ bounds most of the time](assets/ekf_consistency-light.svg#only-light)
![Estimation errors in x, y and heading stay inside the filter's own ±2σ bounds most of the time](assets/ekf_consistency-dark.svg#only-dark)

- The band widens between sensor readings (prediction only) and snaps inward at each reading.
  It is widest where few poles are in view.
- The error (black line) should stay inside ±2σ about 95 % of the time. Over 40 runs it did
  so 95 %, 94 % and 95 % of the time for $x$, $y$ and $\theta$.

The **NEES** (normalized estimation error squared),
$e^\top \Sigma^{-1} e$ with $e$ = truth − estimate, rolls this check into one number. For a
consistent filter it averages to the size of the state, here 3. Over 40 runs it averaged 3.15.
The **NIS** (normalized innovation squared), $\nu^\top S^{-1}\nu$, averages to the size of the
measurement, here 2, and it needs no ground truth, so you can compute it on a real robot.
It averaged 1.99.

If NEES is much larger than 3, your filter is **overconfident**. It will soon start
ignoring measurements, and that is how filters diverge. Typical causes are motion noise set
too small or a wrong Jacobian. If NEES is much smaller than 3, the filter is too cautious and
is wasting information.

## Common mistakes

| Mistake | What you will see |
|---|---|
| Not wrapping the bearing innovation | Errors of several metres as soon as a pole is behind the robot (bearing near ±180°). In this simulation that happens 9–15 s into the lap, and the estimate never recovers |
| A sign error in a Jacobian | The filter still "works" when the robot drives straight, and fails when it turns. The numerical check catches this |
| $R$ and $Q$ swapped (see the warning above) | NEES far from 3; the estimate trusts the wrong source |
| Forgetting $R = V M V^\top$ and adding $M$ directly | A shape error, or motion noise in the wrong units |

## What the EKF cannot do

The EKF keeps one Gaussian, one best guess with an ellipse around it. It relies on the two
conveniences from the start of the lesson:

- **A reasonable initial guess**, so that the linearization is taken near the truth.
- **Knowing which pole is which.** Without labels, the filter has to *guess* which pole it
  sees. A wrong guess feeds it a confident, wrong correction.

Remove them and the robot faces a belief that is not a single blob at all. That's Lesson 4.

## Check yourself

??? question "1. The robot drives straight along x. Why does its y uncertainty grow?"
    Because its heading is uncertain. A heading error $\delta\theta$ over a distance $d$ moves
    the robot sideways by about $d\,\delta\theta$. In the Jacobian, that is the $v\,\Delta t\cos\theta$
    entry in the $(y, \theta)$ position of $G$.

??? question "2. One range-bearing reading of one pole improved the heading estimate. Nothing measures heading directly. How?"
    The bearing depends on the heading, as the $-1$ in $H$ shows. The predicted covariance also
    tied position and heading together (the $0.01$ correlation). The Kalman gain uses both
    connections to distribute the innovation over all three state variables.

??? question "3. Your NIS averages 12 on the real robot. What do you suspect first?"
    The filter's predicted measurement uncertainty $S$ is far too small compared with what the
    innovations actually show. Suspect a sensor noise $Q$ that is too optimistic, motion noise
    that is too small, a Jacobian bug, a missing angle wrap, or readings assigned to the wrong
    landmark.

## Exercises

1. **Break the angle wrap.** Remove `nu[1] = wrap_angle(nu[1])` in `ekf_update` and run a lap.
   Where on the circle does it go wrong, and why there?
2. **An overconfident filter.** In `simulate`, give `ekf_predict` the motion noise `M / 16`
   (standard deviations 4 times too small) while the true noise stays unchanged. Look at the
   NEES, then at the position error. Now imagine a real robot with no ground truth: which
   number would warn you, and how sure could you be?
3. **Bearing-only sensing.** Many cameras measure direction well but distance badly. Drop the
   range from $h$ and $H$ (and $Q$). Does the robot still localize? How many poles would it
   need to see to fix its pose from a single reading, and why does driving around help?
4. **A more realistic simulator.** Simulate the truth with the exact arc motion from
   *Probabilistic Robotics*, but leave the filter's Euler model unchanged. Does the NEES change?

??? tip "What we saw in Exercise 2"
    NEES jumped to between 14 and 32, a clearly overconfident filter. Yet the track still
    looked fine: the largest error was under half a metre, because the poles keep pulling
    the estimate back. Mean NIS, the check you can run without ground truth, rose only from
    about 2.1 to 2.5. A lap has 269 readings, so the standard error of that mean is about
    $\sqrt{2 \cdot 2 / 269} \approx 0.12$ and the rise is real, but you have to know to look.
    An overconfident filter can look perfectly healthy until the poles disappear.

## Go deeper

- **Video:** [Kalman Filter & EKF](https://www.youtube.com/watch?v=E-6paM_Iwfc), a full
  lecture by Cyrill Stachniss (Universität Bonn).
- **Textbook:** Thrun, Burgard & Fox, *Probabilistic Robotics*: Chapter 3 *Gaussian
  Filters* (the EKF), Chapter 5 *Robot Motion*, Chapter 6 *Robot Perception* (the
  range-bearing model) and Chapter 7 *Mobile Robot Localization: Markov and Gaussian*
  (EKF localization, the algorithm in this lesson).
- **Consistency testing:** Y. Bar-Shalom, X. R. Li and T. Kirubarajan, *Estimation with
  Applications to Tracking and Navigation*, Wiley, 2001,
  [doi:10.1002/0471221279](https://doi.org/10.1002/0471221279). The standard reference for
  NEES and NIS tests.
- **Free book:** Roger Labbe, [*Kalman and Bayesian Filters in Python*](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python),
  chapter on the Extended Kalman Filter.

[Next: the particle filter :material-arrow-right:](4-particle-filter.md){ .md-button .md-button--primary }
