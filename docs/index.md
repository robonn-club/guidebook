# Mobile Robotics Guidebook

A graduate-level reference for mobile robotics — covering the probabilistic and algorithmic foundations taught at Universität Bonn, made accessible to anyone.
Maintained by [Robonn](https://robonn.de), the Robotics Club at Universität Bonn.

[New here? Start Here](start-here/index.md){ .md-button .md-button--primary }
[Browse the curriculum](courses/README.md){ .md-button }

---

<p style="font-size:1.5rem; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:-0.02em; margin:1.5rem 0 0.5rem 0;">Start Here: "Where am I?" in four lessons</p>

Learn the idea at the heart of mobile robotics, how a robot stays aware of where it is when
wheels slip and sensors lie, by building it. Each lesson has an interactive demo or
figures to study, a small calculation to do by hand, and a short tested Python program.
No robotics background needed.

<div class="grid cards" markdown>

-   **1 · The Bayes filter**

    ---

    A robot in a hallway works out where it is from "door" and "wall" readings. Try it in
    your browser.

    [Start](start-here/1-bayes-filter.md)

-   **2 · The Kalman filter**

    ---

    Fuse slipping wheels with noisy GPS and beat both. Drag the sliders to see the Kalman gain at work.

    [Start](start-here/2-kalman-filter.md)

-   **3 · The EKF**

    ---

    Localize a 2D robot from range and bearing to landmarks, and test whether your filter
    is telling the truth.

    [Start](start-here/3-ekf-localization.md)

-   **4 · The particle filter**

    ---

    Find the robot with no initial guess and landmarks that all look alike.

    [Start](start-here/4-particle-filter.md)

</div>

<p style="font-size:1.5rem; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:-0.02em; margin:1.5rem 0 0.5rem 0;">Foundations</p>

<div class="grid cards" markdown>

-   **Math & Probability**

    ---

    Probability, Gaussians, Bayes' theorem, linear algebra, coordinate transforms.

    [Open](courses/1_math_and_probability/README.md)

-   **Python for Robotics**

    ---

    NumPy, SciPy, Matplotlib, OpenCV, and ROS2 Python.

    [Open](courses/2_python/README.md)

</div>

<p style="font-size:1.5rem; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:-0.02em; margin:1.5rem 0 0.5rem 0;">Core Curriculum</p>

<div class="grid cards" markdown>

-   **Sensor & Motion Models**

    ---

    Motion models, beam model, likelihood field, and inverse sensor model.

    [Open](courses/3_sensor_motion_models/README.md)

-   **State Estimation**

    ---

    Bayes filter, Kalman filter, EKF, UKF, and particle filter — the complete filter progression.

    [Open](courses/4_state_estimation/README.md)

-   **Localization**

    ---

    Markov localization, EKF localization, and Monte Carlo localization on a known map.

    [Open](courses/5_localization/README.md)

-   **Mapping**

    ---

    Occupancy grids, log-odds representation, OctoMap, and 3D map representations.

    [Open](courses/6_mapping/README.md)

-   **Control & Planning**

    ---

    Robot kinematics, potential fields, A\*, RRT, and path following controllers.

    [Open](courses/11_control_and_planning/README.md)

-   **Computer Vision**

    ---

    Camera models, feature detection, epipolar geometry, deep learning, and temporal tracking.

    [Open](courses/8_computer_vision/README.md)

-   **Inertial Navigation**

    ---

    Strapdown INS mechanization, IMU error modeling, coordinate frames, and INS/GNSS fusion.

    [Open](courses/9_inertial_navigation/README.md)

-   **Global Navigation Satellite Systems**

    ---

    GNSS signals, error sources, RTK, double differencing, and LAMBDA ambiguity resolution.

    [Open](courses/10_global_navigation/README.md)

</div>

<p style="font-size:1.5rem; font-weight:700; font-family:'Outfit',sans-serif; letter-spacing:-0.02em; margin:1.5rem 0 0.5rem 0;">Integration & Advanced</p>

<div class="grid cards" markdown>

-   **SLAM**

    ---

    EKF-SLAM, FastSLAM, graph-based SLAM, loop closure, and modern systems.

    [Open](courses/7_slam/README.md)

-   **Machine Learning**

    ---

    Gaussian processes, deep learning for perception, uncertainty estimation, and RL.

    [Open](courses/12_machine_learning/README.md)

-   **C++ for Robotics**

    ---

    Modern C++, Eigen, g2o, GTSAM, ROS2 C++, and CMake.

    [Open](courses/13_cpp/README.md)

</div>

---

<div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1rem;" markdown>
[License](https://creativecommons.org/licenses/by/4.0/){ .md-button }
[Contribute](CONTRIBUTING.md){ .md-button .md-button--primary }
</div>
