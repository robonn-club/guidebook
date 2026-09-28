# Courses

The curriculum follows the mathematical dependencies of mobile robotics. Each topic assumes the ones listed before it. If you are already comfortable with a topic's prerequisites, you can skip it.

!!! tip "New to mobile robotics?"
    Do the [Start Here](../start-here/index.md) path first. In four hands-on lessons you build
    the filters at the heart of topics 4, 5 and 11, and then this map will make much more sense.

## The "At Bonn" boxes

Universität Bonn runs a dedicated [M.Sc. Mobile Robotics](https://www.moro.uni-bonn.de/)
(MoRo). Where a topic on this site is examined by one of that programme's six mandatory
modules, the page carries an **At Bonn** box naming the module, its credits, its semester,
and its exam format.

The mapping is close. The whole first semester is four mandatory modules —
`MA-MORO-M01` (9 CP), `MA-MORO-M02` (6 CP), `MA-MORO-M03` (6 CP) and `MA-MORO-M04` (9 CP),
exactly 30 CP — and this guidebook covers nearly all of their content. `MA-MORO-M01` on its
own spans six of the thirteen topics below.

!!! warning "Check this against the official manual before you rely on it"

    These boxes are transcribed from the official
    [module manual](https://www.moro.uni-bonn.de/medien_-moro/modulhandbuch-morob-v260227.pdf),
    version **v260227 (27 February 2026)**, and the
    [curriculum page](https://www.moro.uni-bonn.de/in-study/curriculum). Module manuals are
    revised. Never plan an exam around what you read here without confirming it against the
    current manual and the examination office.

    One known inconsistency in the source: the manual's index counts `MA-MORO-M04`
    (Computer Vision) inside the 42 CP mandatory block — and 9 + 6 + 6 + 9 + 6 + 6 = 42
    confirms it — but that module's own allocation table lists it as "Elective selection",
    because it is shared with the Computer Science M.Sc. as `MA-INF 2201`. Confirm your own
    case with the examination office.

    Nothing in these boxes describes what an exam is *like* — only what the manual states.
    That gap is deliberate, and it is
    [yours to fill](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml)
    if you have sat one.

The boxes cover the six mandatory modules only. Electives are out of scope, with one
exception noted on the C++ page.

---

### Phase 1 — Foundation

| # | Topic | Content |
|---|-------|---------|
| 1 | [Math & Probability](1_math_and_probability/README.md) | Probability, Gaussians, Bayes' theorem, linear algebra, coordinate transforms |
| 2 | [Python for Robotics](2_python/README.md) | NumPy, SciPy, Matplotlib, OpenCV, ROS2 Python |

---

### Phase 2 — Core Curriculum

| # | Topic | Requires | Content |
|---|-------|----------|---------|
| 3 | [Sensor & Motion Models](3_sensor_motion_models/README.md) | 1 | Motion models, beam model, likelihood field, inverse sensor model |
| 4 | [State Estimation](4_state_estimation/README.md) | 1, 3 | Bayes filter, Kalman filter, EKF, UKF, particle filter |
| 5 | [Localization](5_localization/README.md) | 3, 4 | Markov localization, EKF localization, Monte Carlo localization |
| 6 | [Mapping](6_mapping/README.md) | 3, 4 | Occupancy grids, log-odds, OctoMap, 3D representations |
| 7 | [Control & Planning](11_control_and_planning/README.md) | 4, 5 | Robot kinematics, potential fields, A\*, RRT, pure pursuit |
| 8 | [Computer Vision](8_computer_vision/README.md) | 1, 2 | Camera models, features, epipolar geometry, deep learning, tracking |
| 9 | [Inertial Navigation](9_inertial_navigation/README.md) | 1, 4 | IMU grades, strapdown mechanization, coordinate frames, INS/GNSS fusion |
| 10 | [Global Navigation Satellite Systems](10_global_navigation/README.md) | 1 | GNSS signals, error sources, RTK, double differencing, LAMBDA |

---

### Phase 3 — Integration & Advanced

| # | Topic | Requires | Content |
|---|-------|----------|---------|
| 11 | [SLAM](7_slam/README.md) | 3–6 | EKF-SLAM, FastSLAM, graph-based SLAM, loop closure, ORB-SLAM3, KISS-ICP |
| 12 | [Machine Learning](12_machine_learning/README.md) | 1, 2 | Gaussian processes, deep learning for perception, uncertainty estimation, RL |
| 13 | [C++ for Robotics](13_cpp/README.md) | 2, 4 | Modern C++, Eigen, g2o, GTSAM, ROS2 C++, CMake |
