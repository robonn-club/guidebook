# SLAM

> Simultaneous Localization and Mapping — estimating both the robot's trajectory and the map of the environment when neither is known.

---

## Topics

**The SLAM Problem**
- Full SLAM — estimate the entire trajectory and map: p(x_{1:t}, m | z_{1:t}, u_{1:t})
- Online SLAM — estimate only the current pose: p(x_t, m | z_{1:t}, u_{1:t})
- Why it is hard: localization requires a map; mapping requires known poses — a circular dependency
- Data association — matching current observations to previously seen landmarks; the hardest part; wrong associations cause catastrophic divergence

**EKF-SLAM**
- State vector: robot pose concatenated with all landmark positions
- Covariance matrix captures correlations between pose and all landmarks — cannot be ignored
- Complexity: O(n²) memory and O(n²) per update step where n = number of landmarks
- Does not scale beyond a few hundred landmarks
- Off-diagonal covariance terms express that landmark estimates are correlated through the trajectory

**FastSLAM — Rao-Blackwellized Particle Filter**
- Key insight: conditioned on the robot trajectory, each landmark is independent of all others
- Rao-Blackwellization: particle filter over trajectories; one EKF per landmark per particle
- Each particle maintains its own map — allows multimodal trajectory distributions
- FastSLAM 1.0 vs. 2.0 — 2.0 uses the current observation to propose better particles
- Particle degeneracy over long trajectories — the fundamental limitation

**Graph-Based SLAM**
- Nodes = robot poses; edges = constraints from odometry and loop closures
- Front-end: building the graph — odometry edges from motion model, loop closure edges from place recognition
- Back-end: nonlinear least squares over all nodes — minimize sum of squared constraint errors
- Information matrix (inverse covariance) is sparse — this is what makes large-scale optimization tractable
- Solvers: g2o (Kümmerle et al.), GTSAM (Dellaert), Ceres

**Loop Closure**
- Without loop closure, drift accumulates unboundedly
- Detection: place recognition — bag-of-words (DBoW2), scan descriptors (M2DP, Scan Context)
- Verification: geometric consistency check before accepting a loop closure as an edge
- Correction: back-end optimization redistributes the accumulated error across the entire graph

**Modern SLAM Systems**
- Feature-based visual SLAM: ORB-SLAM3 — tracks ORB features; handles monocular, stereo, RGB-D, and IMU
- Direct visual SLAM: LSD-SLAM, DSO — uses raw pixel intensities; denser but less robust
- LiDAR odometry and mapping: LOAM, LIO-SAM, KISS-ICP — scan-to-scan and scan-to-map matching
- Visual-Inertial Odometry (VIO): VINS-Mono, Kimera — tightly coupled camera and IMU

---

## Videos

- **Cyrill Stachniss — SLAM lecture series** (YouTube @CyrillStachniss) — covers EKF-SLAM, FastSLAM, and graph-based SLAM with full derivations; the primary reference for this page
- **Cyrill Stachniss — Graph-Based SLAM** (YouTube @CyrillStachniss) — front-end and back-end explained separately; clearest treatment of the information matrix sparsity argument

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapters 10–13: EKF-SLAM, FastSLAM 1.0 and 2.0, graph-based SLAM. The foundational derivations.
- **g2o: A General Framework for Graph Optimization** — Kümmerle et al. (2011) — short paper; explains the sparse solver structure behind graph SLAM back-ends.
- **Factor Graphs and GTSAM: A Hands-on Introduction** — Dellaert (2012) — free technical report; the clearest introduction to factor graph formulation of SLAM.
- **Past, Present, and Future of Simultaneous Localization and Mapping** — Cadena et al. (2016), IEEE T-RO — comprehensive survey of the field; good for understanding where any specific system fits.
