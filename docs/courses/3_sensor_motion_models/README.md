# Sensor & Motion Models

> The two probabilistic models every state estimator depends on — how the robot moves and how it perceives.

---

## Topics

**Motion Models**
- Odometry motion model — converting wheel encoder readings into a probabilistic displacement estimate
- Velocity motion model — using velocity commands (v, ω) when odometry is unavailable
- Sources of motion noise — wheel slip, uneven terrain, encoder resolution
- Representing motion uncertainty as a Gaussian over (Δx, Δy, Δθ)

**Sensor Models**
- Beam model — four components: expected hit, unexpected obstacle, max range, random noise
- Likelihood field model — faster alternative; models sensor as Gaussian around nearest obstacle
- Which model to use and when — beam model is more accurate, likelihood field is more practical
- Inverse sensor model — mapping a range reading back to occupancy probabilities; used in grid mapping

**Landmark / Feature Sensor Model**
- Measuring range and bearing to known landmarks
- Jacobian of the measurement function — required for EKF
- Data association — matching observations to landmarks

---

## Videos

- **Cyrill Stachniss — Mobile Robotics, Lecture 4: Motion Models** (YouTube @CyrillStachniss) — derives both odometry and velocity models from scratch
- **Cyrill Stachniss — Mobile Robotics, Lecture 5: Sensor Models** (YouTube @CyrillStachniss) — beam model and likelihood field model with worked examples

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 5: *Robot Motion* and Chapter 6: *Robot Perception*. These two chapters are the definitive reference; everything on this page comes from them.
- **Introduction to Autonomous Mobile Robots** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 4: *Perception*. More hardware-focused treatment of sensor characteristics.
