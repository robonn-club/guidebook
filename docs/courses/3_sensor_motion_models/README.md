# Sensor & Motion Models

> The two probabilistic models every state estimator depends on — how the robot moves and how it perceives.

!!! info "At Bonn — MA-MORO-M01"

    Examined in **Introduction to Mobile Robotics** (`MA-MORO-M01`), 9 CP, 1st semester —
    the manual lists "probabilistic motion models, probabilistic sensor models" among its
    contents. Two written exams: 120 min (67%) and 60 min (33%). You need at least 50% of the
    exercise points to be admitted to them.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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

- **[Motion Models](https://www.youtube.com/watch?v=IVTV7vJgIkU)** — Nived Chebrolu (StachnissLab, Uni Bonn) — derives both the odometry and velocity models from scratch
- **[Observation Models](https://www.youtube.com/watch?v=SfwxLpdFB-o)** — Cyrill Stachniss — beam model and likelihood field model with worked examples

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 5: *Robot Motion* and Chapter 6: *Robot Perception*. These two chapters are the definitive reference; everything on this page comes from them.
- **[Introduction to Autonomous Mobile Robots](https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/)** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 4: *Perception*. More hardware-focused treatment of sensor characteristics.
