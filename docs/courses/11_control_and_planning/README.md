# Control & Planning

> How a mobile robot moves through the world — from kinematic models and reactive controllers to global path planners.

---

## Topics

**Robot Kinematics**
- Differential drive model — relate wheel velocities (v_l, v_r) to body velocity (v, ω)
- Car-like (Ackermann) model — steering angle constrains turning radius; minimum turning radius
- Non-holonomic constraints — mobile robots cannot move sideways; planning must respect this
- Kinematic equations of motion — forward model: how (v, ω) propagates (x, y, θ)
- Motion primitives — discretizing the control space for planning

**Reactive Control**
- Potential field navigation — attractive potential toward goal, repulsive potential from obstacles
- Gradient descent on the combined field gives the control input
- Local minima — the fundamental failure mode; robot gets trapped in saddle points
- Bug algorithms — guaranteed to reach goal by following obstacle boundaries; simple but slow

**Path Planning — Graph-Based**
- Configuration space (C-space) — representing robot state including orientation; obstacles in C-space vs. workspace
- Grid-based planning — discretize C-space; Dijkstra for optimal paths; A* with heuristic for faster search
- D* and D*-Lite — replanning when the map changes; used in real navigation stacks
- Voronoi roadmaps — plan in the maximally safe region equidistant from all obstacles

**Path Planning — Sampling-Based**
- Probabilistic Roadmap (PRM) — sample random configurations, connect nearby pairs, query the graph
- Rapidly-exploring Random Tree (RRT) — grow a tree by sampling and steering; single-query planner
- RRT* — asymptotically optimal variant; rewires the tree to improve path cost over time
- Non-holonomic RRT — steering function must respect kinematic constraints; not simple Euclidean extension

**Path and Trajectory Following**
- Pure pursuit controller — look-ahead point on the path; steer toward it; simple and effective
- Stanley controller — combines heading error and cross-track error; used in the DARPA challenge winner
- Model Predictive Control (MPC) — optimize a trajectory over a receding horizon; handles constraints explicitly; computationally expensive

---

## Videos

- **Cyrill Stachniss — Mobile Robotics, Lectures on Motion and Planning** (YouTube @CyrillStachniss) — kinematics, potential fields, grid planning, and RRT with worked examples
- **Sebastian Thrun — Artificial Intelligence for Robotics** (Udacity / YouTube) — A*, RRT, and PID in a robotics context; accessible entry point

---

## Book / Article Resources

- **Planning Algorithms** — LaValle (2006) — free online at planning.cs.uiuc.edu; the definitive reference for configuration space, PRM, RRT, and all planning variants covered here
- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 5: *Robot Motion*; kinematic models for differential drive and car-like robots
- **Introduction to Autonomous Mobile Robots** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 3: *Mobile Robot Kinematics* and Chapter 6: *Navigation*; more accessible than LaValle for the kinematics sections
