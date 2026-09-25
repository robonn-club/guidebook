# Courses

The curriculum follows the mathematical dependencies of mobile robotics. Each topic assumes the ones listed before it. If you are already comfortable with a topic's prerequisites, you can skip it.

!!! tip "New to mobile robotics?"
    Do the [Start Here](../start-here/index.md) path first. In four hands-on lessons you build
    the filters at the heart of topics 4, 5 and 11, and then this map will make much more sense.

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
