# Mapping

> Building a representation of the environment from sensor data — assuming the robot's poses are known.

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

- **Cyrill Stachniss — Mobile Robotics, Lecture: Occupancy Grid Mapping** (YouTube @CyrillStachniss) — derives the log-odds update from Bayes' rule; the clearest treatment available
- **Cyrill Stachniss — OctoMap and 3D Mapping** (YouTube @CyrillStachniss) — covers 3D representations and the memory vs. resolution trade-off

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 9: *Occupancy Grid Mapping*. Derives log-odds from scratch; read this before writing any mapping code.
- **OctoMap: An Efficient Probabilistic 3D Mapping Framework** — Hornung et al. (2013) — the original paper; short and readable; explains the octree structure and probabilistic update rule.
- **Introduction to Autonomous Mobile Robots** — Siegwart, Nourbakhsh, Scaramuzza (2011) — Chapter 6: *Mapping*. Broader overview of map types before going deep on grids.
