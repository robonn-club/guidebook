# Localization

> Given a map, where is the robot? — estimating pose from sensor data when the environment is already known.

---

## Topics

**The Localization Problem**
- Position tracking vs. global localization vs. kidnapped robot — three difficulty levels
- Belief representation — why a single pose estimate is insufficient; we need a distribution

**Markov Localization**
- Discrete grid-based belief over all possible poses
- Prediction step — applying the motion model to propagate belief
- Correction step — weighting grid cells by sensor likelihood
- Computational cost — why discrete grids do not scale to 3D

**EKF Localization**
- Continuous Gaussian belief — mean pose vector and covariance matrix
- Prediction step using the odometry motion model and Jacobian
- Correction step using the landmark measurement model and Jacobian
- Data association — the hard part; matching observations to known landmarks
- Limitations — Gaussian assumption breaks down for global localization

**Monte Carlo Localization (MCL)**
- Particle set as a non-parametric belief representation
- Importance sampling — weight each particle by measurement likelihood
- Resampling — focus particles on high-probability regions
- Global localization — starting with uniform particle distribution over the entire map
- Particle degeneracy — what goes wrong without resampling; low-variance resampling as a fix
- Adaptive MCL — dynamically adjusting particle count based on filter uncertainty

---

## Hands-on

Build all three yourself in the [Start Here](../../start-here/index.md) path:
[Markov localization in a hallway](../../start-here/1-bayes-filter.md) ·
[EKF localization](../../start-here/3-ekf-localization.md) ·
[Monte Carlo localization from an unknown start](../../start-here/4-particle-filter.md).

---

## Videos

- **Cyrill Stachniss — [Kalman Filter & EKF](https://www.youtube.com/watch?v=E-6paM_Iwfc)** — the filter behind EKF localization
- **Cyrill Stachniss — [Particle Filter and Monte Carlo Localization](https://www.youtube.com/watch?v=MsYlueVDLI0)** — MCL with derivations, resampling, and practical details

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 7: *Mobile Robot Localization: Markov and Gaussian*, Chapter 8: *Mobile Robot Localization: Grid and Monte Carlo*. The reference implementations of all algorithms on this page.
- **Introduction to Autonomous Mobile Robots** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 5: *Mobile Robot Localization*. More accessible introduction before diving into Thrun.
