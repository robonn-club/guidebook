# Inertial Navigation Systems (INS)

> Estimating position, velocity, and attitude from accelerometers and gyroscopes alone — self-contained navigation that works anywhere but drifts over time.

!!! info "At Bonn — MA-MORO-M02"

    Examined in **Trajectory Estimation** (`MA-MORO-M02`), 6 CP, 1st semester — the manual
    lists "inertial sensors, accelerometer, gyroscope, IMU, magnetometer", odometry and
    inertial navigation among its contents. Two written exams of 60 min, 50% each; admission to
    both requires successful completion of the exercises with at least 50% of the points.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

---

## Topics

**IMU Hardware and Grades**
- Accelerometers — measuring specific force (not absolute acceleration; gravity included)
- Gyroscopes — measuring angular rate; MEMS, fiber optic (FOG), ring laser (RLG)
- IMU grades: consumer → tactical → navigation → strategic — each decade of improvement costs ~100× more; choose based on mission duration and accuracy requirement
- Magnetometers and barometers as low-cost aiding sensors

**Coordinate Frames**
- Body frame (b-frame) — fixed to the IMU; axes aligned with sensor measurement axes
- Navigation frame (n-frame) — local level frame; North-East-Down (NED) or East-North-Up (ENU)
- Earth-Centered Earth-Fixed (ECEF, e-frame) — origin at Earth's center, rotates with Earth
- Earth-Centered Inertial (ECI, i-frame) — non-rotating; Newton's laws apply here
- Transformations between frames — rotation matrices C_b^n, C_n^e; must be tracked at every step

**Attitude Representation**
- Euler angles (roll, pitch, yaw) — intuitive but suffer from gimbal lock; not used in mechanization
- Direction cosine matrix (DCM) — 3×3 rotation matrix; numerically stable but has 9 elements with 6 constraints
- Quaternions — 4-element unit quaternion; compact, no singularity; standard for strapdown algorithms

**Strapdown INS Mechanization**
- Attitude update — integrate angular rate to propagate the rotation from b-frame to n-frame
- Specific force transformation — rotate accelerometer output from b-frame to n-frame
- Velocity update — subtract gravity, integrate specific force to get velocity in n-frame
- Position update — integrate velocity; for global navigation use ECEF equations
- Coning and sculling corrections — numerical errors from finite step size; critical at high update rates

**IMU Error Modeling**
- Deterministic errors — bias offset, scale factor, axis misalignment; calibrated in lab
- Stochastic errors — angle random walk (ARW), rate random walk (RRW), bias instability
- Allan variance — log-log plot of deviation vs. averaging time; identifies ARW, bias instability, and RRW from flat noise floor regions; the standard IMU characterization tool
- Error growth: position error from gyro drift grows as t³; from accelerometer bias grows as t²

**Initial Alignment**
- Coarse alignment — leveling (from accelerometers) and gyrocompassing (from Earth-rate gyroscopes)
- Fine alignment — Kalman filter to estimate residual errors; required before navigation
- Transfer alignment — aligning a slave IMU to a master system in dynamic conditions

**INS/GNSS Integration**
- Loosely coupled — GNSS position and velocity as Kalman filter observations
- Tightly coupled — GNSS pseudoranges and Doppler directly as observations; works with fewer than 4 satellites
- Ultra-tight coupling — feedback into GNSS signal tracking loops; maximum robustness
- Error state (indirect) Kalman filter — estimating INS error states (δp, δv, δψ, δb_a, δb_g) rather than full states; standard approach

---

## Videos

- **[Mobile Sensing and Robotics 2](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQh_J16IMwDlji18SWQ2PZ6)** — Cyrill Stachniss (Uni Bonn) — sensors and state estimation, including IMU characteristics and sensor fusion
- **[Kalibr — IMU noise model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model)** (ETH Zurich) — practical guide to IMU noise parameter estimation using Allan variance; the reference used by most VIO pipelines
- **Lasse Klingbeil — Navigation Systems lectures** (IGG, Universität Bonn) — strapdown mechanization, error modeling, and GNSS/INS integration; taught in Bonn, recordings not public

---

## Book / Article Resources

- **[Strapdown Inertial Navigation Technology](https://doi.org/10.1049/PBRA017E)** — Titterton & Weston (2004) — the standard reference for strapdown mechanization; covers all coordinate frame equations and error models in detail
- **[Navigation Using Inertial Sensors](https://discovery.ucl.ac.uk/id/eprint/1470141/)** — Paul Groves (2015), IEEE AESS tutorial — free from UCL Discovery; a compact, self-contained tutorial on the principles before committing to a textbook
- **Aided Navigation: GPS with High Rate Sensors** — Jay Farrell (2008) — covers the error-state Kalman filter for INS/GNSS fusion; mathematical treatment is directly implementable
- **Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems** — Groves (2nd ed., 2013), Artech House — comprehensive; covers all integration architectures including tightly coupled and ultra-tight
