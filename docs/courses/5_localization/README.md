# Localization

> Given a map, where is the robot? — estimating pose from sensor data when the environment is already known.

!!! info "At Bonn — MA-MORO-M01"

    Examined in **Introduction to Mobile Robotics** (`MA-MORO-M01`), 9 CP, 1st semester —
    the manual lists "localization" and "particle filter" among its contents. Two written exams: 120 min (67%) and 60 min (33%). You need at least 50% of the
    exercise points to be admitted to them.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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

- **[EKF Localization](https://www.youtube.com/watch?v=PiCC-SxWlH8)** — Nived Chebrolu (StachnissLab, Uni Bonn) — the EKF applied to localization against a known map
- **[Particle Filter and Monte Carlo Localization](https://www.youtube.com/watch?v=MsYlueVDLI0)** — Cyrill Stachniss — resampling strategies and practical implementation details
- **[Localization — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=TLe4otkRAts)** — the problem statement in five minutes; watch first if the topic is new
- **[Mobile Sensing and Robotics 1](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQEn33QDVGJpiZLi-SlL7vA)** — Cyrill Stachniss (Uni Bonn) — the full course; covers Markov, EKF, and Monte Carlo localization with derivations

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 7: *Mobile Robot Localization: Markov and Gaussian*, Chapter 8: *Mobile Robot Localization: Grid and Monte Carlo*. The reference implementations of all algorithms on this page.
- **[Introduction to Autonomous Mobile Robots](https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/)** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 5: *Mobile Robot Localization*. More accessible introduction before diving into Thrun.
