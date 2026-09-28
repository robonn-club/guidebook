# SLAM

> Simultaneous Localization and Mapping — estimating both the robot's trajectory and the map of the environment when neither is known.

!!! info "At Bonn — MA-MORO-M01 and MA-MORO-M05"

    You meet SLAM twice. `MA-MORO-M01` (9 CP, 1st semester) covers "basics of simultaneous
    localization and mapping (SLAM); SLAM with kalman and particle filters" — two written
    exams, 120 min (67%) and 60 min (33%), admission requires ≥50% of the exercise points.
    **Robot Mapping** (`MA-MORO-M05`, 6 CP, 2nd semester) covers the graph-based half:
    "graph-based simultaneous localization and mapping; robust least squares; hierarchical
    optimization approaches" and bundle adjustment — two written exams of 60 min, 50% each,
    again gated on ≥50% of the exercise points.

    *Sat either exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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

- **[Introduction to SLAM](https://www.youtube.com/watch?v=0I30M6yTklo)** — Cyrill Stachniss — what the problem is and why it is hard; the right starting point
- **[Graph-based SLAM using Pose Graphs](https://www.youtube.com/watch?v=uHbRKvD8TWg)** — Cyrill Stachniss — front-end and back-end explained separately; clearest treatment of the information matrix sparsity argument
- **[Graph-Based SLAM with Landmarks](https://www.youtube.com/watch?v=mZBdPgBtrCM)** — Cyrill Stachniss — extends the pose graph with landmark nodes
- **[SLAM Course (2013)](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQrZ4O5QzbIHgl3b1JHimN_)** — Cyrill Stachniss — the full 21-lecture course; covers EKF-SLAM, FastSLAM, and graph-based SLAM with complete derivations

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapters 10–13: EKF-SLAM, FastSLAM 1.0 and 2.0, graph-based SLAM. The foundational derivations.
- **[g2o: A General Framework for Graph Optimization](http://ais.informatik.uni-freiburg.de/publications/papers/kuemmerle11icra.pdf)** — Kümmerle et al. (2011) — short paper; explains the sparse solver structure behind graph SLAM back-ends.
- **[Factor Graphs and GTSAM: A Hands-on Introduction](https://www.cc.gatech.edu/~dellaert/pubs/Dellaert12techreport.pdf)** — Dellaert (2012) — free technical report; the clearest introduction to the factor graph formulation of SLAM.
- **[Past, Present, and Future of Simultaneous Localization and Mapping](https://arxiv.org/abs/1606.05830)** — Cadena et al. (2016), IEEE T-RO — comprehensive survey of the field; good for understanding where any specific system fits.
