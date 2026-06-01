# Python

> Python is the prototyping language of robotics research — you implement an algorithm, verify it works, then hand it off to C++ if it needs to run in real-time.

---

## Topics

**NumPy — the foundation**
- Arrays vs. lists — always use arrays for numerical work
- Array creation, slicing, broadcasting rules
- `np.linalg` — matrix inverse, solve, SVD, eigendecomposition
- Vectorization — replacing for-loops with array operations
- Indexing with boolean masks

**SciPy**
- `scipy.linalg` — more robust than `np.linalg` for ill-conditioned matrices
- `scipy.optimize` — least squares (`least_squares`), nonlinear minimization (`minimize`)
- `scipy.spatial.transform.Rotation` — SO(3) rotations, quaternions, Euler angles; use this instead of writing your own

**Matplotlib**
- Line plots, scatter plots, subplots
- Plotting 2D robot trajectories and covariance ellipses
- Animating filter updates over time
- `plt.pause()` for real-time visualization in scripts

**OpenCV (cv2)**
- Image loading, color conversion, resizing
- Feature detection — ORB, SIFT
- Camera calibration with `cv2.calibrateCamera`
- Drawing on images — landmarks, trajectories, bounding boxes

**ROS2 — rclpy**
- Node lifecycle — `rclpy.init`, `Node`, `spin`, `destroy_node`
- Publishers and subscribers — `create_publisher`, `create_subscription`
- Timers — `create_timer` for periodic callbacks
- Services and actions for request-response patterns

---

## Videos

- **Cyrill Stachniss — programming exercises** (YouTube @CyrillStachniss) — Python implementations accompanying the mobile robotics lecture series
- **NumPy official quickstart** (numpy.org/doc) — 30-minute read; covers 80% of what you need
- **Sentdex — Matplotlib tutorials** (YouTube @sentdex) — practical and fast

---

## Book / Article Resources

- **[NumPy documentation](https://numpy.org/doc/stable/)** — the quickstart and the `linalg` module reference
- **[SciPy documentation](https://docs.scipy.org/doc/scipy/)** — especially `spatial.transform` and `optimize`
- **[ROS2 rclpy API](https://docs.ros2.org/latest/api/rclpy/)** — reference for all node, publisher, and subscriber calls
- **Python for Data Analysis** — Wes McKinney — chapters on NumPy and vectorization; ignore the pandas parts
