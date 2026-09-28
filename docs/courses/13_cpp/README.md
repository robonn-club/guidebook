# C++

> C++ is where the algorithms from this guidebook run in production — state estimators, scan matchers, and graph optimizers all require the performance and control that Python cannot provide.

!!! warning "At Bonn — elective, not mandatory"

    No mandatory MoRo module teaches C++. It is available as the elective **Modern C++ for
    Robotics and Computer Vision** (`MA-MORO-E03`, 6 CP), whose contents include modern
    CMake, memory management, the STL, generic programming, LiDAR mapping and 3D point cloud
    processing. Electives are otherwise outside the scope of these boxes.

---

## Topics

**Modern C++ (C++17)**
- Types and memory model — stack vs. heap, RAII, scope-based cleanup
- References and pointers — `const&`, `unique_ptr`, `shared_ptr`
- STL containers — `vector`, `map`, `unordered_map`, `deque`
- Range-based for, structured bindings, `auto`
- Lambdas — capturing by value and reference

**Eigen — linear algebra**
- Dense matrix types — `MatrixXd`, `Matrix3d`, `VectorXd`, `Vector3d`
- Solving linear systems — `ldlt().solve()`, `jacobiSvd()`
- Rigid body transforms — `Isometry3d`, `AngleAxisd`, `Quaterniond`
- Mapping raw arrays to Eigen — `Eigen::Map`
- Sparse matrices — `SparseMatrix<double>` used in graph optimization

**Graph Optimization Libraries**
- **g2o** — general graph optimizer; used throughout SLAM research; understand vertices, edges, and the `optimize()` call
- **GTSAM** — Georgia Tech Smoothing and Mapping; factor graph formulation; strong for VIO and large-scale SLAM
- **Ceres Solver** — Google's nonlinear least squares; used in LiDAR odometry systems (e.g., Cartographer)

**Point Cloud Library (PCL)**
- `pcl::PointCloud<pcl::PointXYZ>` — the core data structure
- Filtering — voxel grid, passthrough, statistical outlier removal
- Registration — ICP (`pcl::IterativeClosestPoint`), NDT
- Integrates with ROS2 via `pcl_conversions`

**Build System**
- CMake — `find_package`, `target_link_libraries`, `add_executable`
- `compile_commands.json` — generate with `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` for clangd
- `colcon build` — ROS2 workspace builds; understand overlay and underlay workspaces

**ROS2 — rclcpp**
- `rclcpp::Node`, `create_publisher<T>`, `create_subscription<T>`
- Timers, services, actions
- `tf2` — broadcasting and listening to coordinate frame transforms

---

## Videos

- **[Back to Basics: Smart Pointers](https://www.youtube.com/watch?v=xGDLkt-jBJ4)** — Arthur O'Dwyer, CppCon 2019 — covers `unique_ptr` and `shared_ptr` clearly
- **[Back to Basics: Move Semantics (part 1)](https://www.youtube.com/watch?v=St0MNEU5b0o)** and **[(part 2)](https://www.youtube.com/watch?v=pIzaZbKUw2s)** — Klaus Iglberger, CppCon 2019 — essential for understanding how Eigen and STL containers work efficiently
- **Articulated Robotics — ROS2 in C++** (YouTube @ArticulatedRobotics) — practical node writing with rclcpp

---

## Book / Article Resources

- **[Eigen documentation](https://eigen.tuxfamily.org/dox/)** — the module guide and the *Getting Started* page; the API docs are comprehensive
- **[g2o — A General Framework for Graph Optimization](https://github.com/RainerKuemmerle/g2o)** — read [the paper](http://ais.informatik.uni-freiburg.de/publications/papers/kuemmerle11icra.pdf) (Kümmerle et al., 2011) before diving into the code
- **[GTSAM tutorials](https://gtsam.org/tutorials/intro.html)** — the factor graph introduction is the clearest explanation of graph-based SLAM available
- **[cppreference.com](https://en.cppreference.com/)** — authoritative reference for the standard library
- **[ROS2 C++ documentation](https://docs.ros.org/en/jazzy/index.html)** — the rclcpp tutorials; start from *Writing a simple publisher and subscriber*
- **Effective Modern C++** — Scott Meyers (2014), O'Reilly — items on smart pointers, move semantics, and lambdas are directly applicable
