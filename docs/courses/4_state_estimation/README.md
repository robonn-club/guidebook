# State Estimation

> Estimating what cannot be directly measured — a robot's pose, velocity, or map — by recursively fusing motion predictions with sensor observations under uncertainty.

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
- The Kalman gain K is the derived in topic 1 — it decides how much to trust the measurement

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

## Videos

- **Cyrill Stachniss — Bayes Filter** (YouTube @CyrillStachniss) — derives the predict-correct recursion from probability theory; watch before any other filter lecture
- **Cyrill Stachniss — Kalman Filter** (YouTube @CyrillStachniss) — derives KF as a special case of the Bayes filter under linear Gaussian assumptions
- **Cyrill Stachniss — Extended Kalman Filter** (YouTube @CyrillStachniss) — Jacobian linearization with a concrete 2D robot example
- **Cyrill Stachniss — Particle Filter** (YouTube @CyrillStachniss) — importance sampling, resampling strategies, and failure modes

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 3: *Gaussian Filters* (KF, EKF, UKF) and Chapter 4: *Nonparametric Filters* (particle filter). The derivations here follow this book directly.
- **State Estimation for Robotics** — Barfoot (2017) — deeper treatment of the EKF and batch estimation; covers Lie group formulations used in modern SLAM.
- **Optimal State Estimation** — Dan Simon (2006) — comprehensive reference for KF theory; covers derivations, stability, and practical tuning in detail.
