# Mapping

> Building a representation of the environment from sensor data — assuming the robot's poses are known.

!!! info "At Bonn — MA-MORO-M01 and MA-MORO-M05"

    Split across two semesters. `MA-MORO-M01` (9 CP, 1st semester) covers "occupancy
    mapping" — two written exams, 120 min (67%) and 60 min (33%), admission requires ≥50%
    of the exercise points. **Robot Mapping** (`MA-MORO-M05`, 6 CP, 2nd semester) goes
    further into "point cloud registration and iterative closest point", 3D sensors and
    mobile mapping — two written exams of 60 min, 50% each, again gated on ≥50% of the
    exercise points. M05 recommends having done M01.

    *Sat either exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

---

## Topics

**Map Representations**
- Feature maps — landmarks with positions and descriptors; compact but sparse
- Metric maps — dense spatial representations (grids, point clouds, meshes)
- Topological maps — graph of places and connections; compact but hard to build
- Which to use: feature maps for EKF-SLAM, metric maps for navigation and MCL

**Occupancy Grid Mapping**
- Grid cells as independent binary random variables — occupied or free
- Why assuming independence is wrong but still works in practice
- The forward sensor model — p(z | map, pose): probability of a measurement given the map
- Inverse sensor model — p(map | z, pose): updating the grid from a single range reading
- Three regions per beam: free (cells along the ray), occupied (endpoint), unknown (beyond)

**Log-Odds Representation**
- Why probabilities are not stored directly — numerical instability near 0 and 1
- Log-odds: l = log(p / (1-p)); additive updates, no multiplication
- Updating a cell: l_t = l_{t-1} + l_sensor - l_prior
- Converting back to probability when needed: p = 1 - 1/(1 + exp(l))
- Clamping — preventing cells from becoming permanently certain

**3D Mapping**
- Extending occupancy grids to 3D — memory cost grows as O(n³)
- OctoMap — octree structure; only allocates memory where obstacles exist
- Point cloud accumulation — concatenating LiDAR scans; requires accurate pose
- Elevation maps — 2.5D; efficient for outdoor terrain, not indoor multi-floor

---

## Videos

- **[Occupancy Grid Maps](https://www.youtube.com/watch?v=v-Rm9TUG9LA)** — Cyrill Stachniss — derives the log-odds update from Bayes' rule; the clearest treatment available
- **[Occupancy Grid — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=8ckhPViqneg)** — the idea in five minutes before the full derivation
- **[Point Cloud Alignment using ICP](https://www.youtube.com/watch?v=djnd502836w)** — Cyrill Stachniss — how the scans that build a 3D map get registered to each other

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 9: *Occupancy Grid Mapping*. Derives log-odds from scratch; read this before writing any mapping code.
- **[OctoMap: An Efficient Probabilistic 3D Mapping Framework](https://doi.org/10.1007/s10514-012-9321-0)** — Hornung et al. (2013) — the original paper; short and readable; explains the octree structure and probabilistic update rule.
- **[OctoMap — library and documentation](https://octomap.github.io/)** — the implementation the paper describes; the docs double as a practical guide to 3D occupancy mapping.
- **[Introduction to Autonomous Mobile Robots](https://mitpress.mit.edu/9780262015356/introduction-to-autonomous-mobile-robots/)** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 6: *Mapping*. Broader overview of map types before going deep on grids.
