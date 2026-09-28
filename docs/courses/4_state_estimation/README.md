# State Estimation

> Estimating what cannot be directly measured — a robot's pose, velocity, or map — by recursively fusing motion predictions with sensor observations under uncertainty.

!!! info "At Bonn — MA-MORO-M01 and MA-MORO-M02"

    Examined twice over, which makes this the highest-leverage page on the site for a first
    semester.

    **Introduction to Mobile Robotics** (`MA-MORO-M01`, 9 CP, 1st semester) covers "Bayes
    filter, state estimation, Kalman filter, extended Kalman filter, particle filter".
    Two written exams: 120 min (67%) and 60 min (33%). You need at least 50% of the
    exercise points to be admitted to them.

    **Trajectory Estimation** (`MA-MORO-M02`, 6 CP, 1st semester) covers the Kalman filter,
    EKF and smoothing again, this time for navigation. Two written exams of 60 min, 50% each,
    with the same ≥50% exercise-points gate.

    *Sat either exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

---

## Topics

**The Bayes Filter — the general framework**
- Recursive state estimation — maintaining a belief distribution over time
- Prediction step — applying the motion model: bel⁻(x_t) = ∫ p(x_t | u_t, x_{t-1}) bel(x_{t-1}) dx_{t-1}
- Correction step — weighting by sensor likelihood: bel(x_t) ∝ p(z_t | x_t) · bel⁻(x_t)
- Every filter in this section is a specific implementation of this framework

**Kalman Filter (KF)**
- Closed-form solution for linear systems with Gaussian noise — exact, not approximate
- State transition: x_t = A x_{t-1} + B u_t + ε, with ε ~ N(0, R)
- Measurement model: z_t = C x_t + δ, with δ ~ N(0, Q)
- Predict: propagate mean and covariance through A
- Update: compute Kalman gain K, correct mean and covariance from residual (z - Cx)
- The Kalman gain K comes from the product of two Gaussians (topic 1) — it decides how much to trust the measurement

**Extended Kalman Filter (EKF)**
- Nonlinear motion or measurement functions — f(x, u), h(x)
- Linearization by first-order Taylor expansion — Jacobians F and H replace A and C
- Same predict-update structure as KF; Jacobians recomputed at each step
- Works well when nonlinearity is mild; diverges when linearization error is large
- The most widely used filter in robotics — EKF-SLAM, EKF localization, INS/GNSS fusion

**Unscented Kalman Filter (UKF)**
- Sigma point approach — propagate a small set of carefully chosen points through the nonlinear function
- Captures mean and covariance to third-order accuracy vs. EKF's first-order
- No Jacobians required — simpler to implement for complex models
- More robust than EKF for strongly nonlinear systems; higher computational cost

**Particle Filter**
- Non-parametric belief representation — a set of weighted samples {x_i, w_i}
- Can represent arbitrary distributions, including multimodal beliefs
- Predict: propagate each particle through the motion model with added noise
- Update: weight each particle by p(z | x_i); normalize weights
- Resample: draw new particle set proportional to weights — eliminates low-weight particles
- Degeneracy — why naive resampling fails; low-variance resampling as the standard fix
- Computational cost scales with the number of particles needed to cover the state space

---

## Hands-on

The [Start Here](../../start-here/index.md) path implements every filter on this page in short, tested Python programs:
[Bayes filter](../../start-here/1-bayes-filter.md) ·
[Kalman filter](../../start-here/2-kalman-filter.md) ·
[EKF](../../start-here/3-ekf-localization.md) ·
[particle filter](../../start-here/4-particle-filter.md).

---

## Videos

- **[Bayes Filter](https://www.youtube.com/watch?v=0lKHFJpaZvE)** — Cyrill Stachniss — derives the predict-correct recursion from probability theory; watch before any other filter lecture
- **[Kalman Filter & EKF](https://www.youtube.com/watch?v=E-6paM_Iwfc)** — Cyrill Stachniss — derives the KF as a special case of the Bayes filter, then linearizes it into the EKF
- **[Particle Filter and Monte Carlo Localization](https://www.youtube.com/watch?v=MsYlueVDLI0)** — Cyrill Stachniss — importance sampling, resampling strategies, and failure modes
- **[Particle Filter — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=YBeVDxTHiYM)** — the five-minute version; good for a first pass or a refresher

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 3: *Gaussian Filters* (KF, EKF, UKF) and Chapter 4: *Nonparametric Filters* (particle filter). The derivations here follow this book directly.
- **[State Estimation for Robotics](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf)** — Barfoot (2017) — deeper treatment of the EKF and batch estimation; covers Lie group formulations used in modern SLAM. Free PDF from the author.
- **[Optimal State Estimation](https://doi.org/10.1002/0470045345)** — Dan Simon (2006) — comprehensive reference for KF theory; covers derivations, stability, and practical tuning in detail.
