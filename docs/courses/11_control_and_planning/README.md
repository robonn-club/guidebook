# Control & Planning

> How a mobile robot moves through the world — from kinematic models and reactive controllers to global path planners.

!!! info "At Bonn — MA-MORO-M01"

    Examined in **Introduction to Mobile Robotics** (`MA-MORO-M01`), 9 CP, 1st semester.
    This page maps onto the module's second half, "Robot Planning and Control": theory of
    dynamic systems, basics of control theory, kinematic models for wheeled robots, digital
    control, P/PD/PID controllers, model predictive control, trajectory control, motion and
    roadmap planning, and Markov decision processes. Two written exams: 120 min (67%) and 60 min (33%). You need at least 50% of the
    exercise points to be admitted to them.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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
- Local minima — the fundamental failure mode; the robot gets trapped where attractive and repulsive forces cancel before it reaches the goal
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

- **[Robot Motion Planning using A*](https://www.youtube.com/watch?v=HR1TNa8Lp7w)** — Cyrill Stachniss — grid-based planning and the heuristic that makes A* admissible
- **[Mobile Sensing and Robotics 1](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQEn33QDVGJpiZLi-SlL7vA)** — Cyrill Stachniss (Uni Bonn) — kinematics and motion planning in the context of the full mobile robotics course

---

## Book / Article Resources

- **[Planning Algorithms](http://lavalle.pl/planning/)** — LaValle (2006) — free online from the author; the definitive reference for configuration space, PRM, RRT, and all planning variants covered here
- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 5: *Robot Motion*; kinematic models for differential drive and car-like robots
- **[Introduction to Autonomous Mobile Robots](https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/)** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 3: *Mobile Robot Kinematics* and Chapter 6: *Navigation*; more accessible than LaValle for the kinematics sections
