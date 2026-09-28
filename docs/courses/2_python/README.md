# Python

> Python is the prototyping language of robotics research — you implement an algorithm, verify it works, then hand it off to C++ if it needs to run in real-time.

!!! info "At Bonn — MA-MORO-M03"

    Taught as **Python for Robotics and Computer Vision** (`MA-MORO-M03`), 6 CP, 1st
    semester. Assessed in two parts: tasks accompanying the semester (90 min, 40%) and a
    written exam (120 min, 60%), with completed exercises required.

    Worth knowing before you arrive: `MA-MORO-M01` runs in the **same semester** and already
    recommends "basic programming skills in Python" for its homework — while M03 is still
    teaching the language from variables upward. Turning up with working Python helps.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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

- **[Mobile Sensing and Robotics 1 — course page](https://www.ipb.uni-bonn.de/msr1-2021/index.html)** — Cyrill Stachniss (Uni Bonn) — lecture recordings alongside the Python programming exercises that accompany the mobile robotics series
- **[Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)** — Andrej Karpathy — not robotics, but the best demonstration of writing numerical Python that you actually understand line by line

---

## Book / Article Resources

- **[NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)** — 30-minute read; covers 80% of what you need
- **[NumPy documentation](https://numpy.org/doc/stable/)** — the quickstart and the `linalg` module reference
- **[SciPy documentation](https://docs.scipy.org/doc/scipy/)** — especially `spatial.transform` and `optimize`
- **[Matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html)** — the official tutorials; start with *Pyplot* then *Artist* if you need custom plots
- **[ROS2 rclpy API](https://docs.ros2.org/latest/api/rclpy/)** — reference for all node, publisher, and subscriber calls
- **[ROS2 documentation](https://docs.ros.org/en/jazzy/index.html)** — the tutorials are the fastest way from zero to a working node
- **[Python for Data Analysis](https://wesmckinney.com/book/)** — Wes McKinney — free online; chapters on NumPy and vectorization; ignore the pandas parts
