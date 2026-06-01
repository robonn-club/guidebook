# Math & Probability

> The two languages of mobile robotics — linear algebra to represent the world, probability theory to represent uncertainty about it.

---

## Topics

**Linear Algebra**
- Vectors and matrices — notation, operations, geometric meaning
- Matrix inverse, transpose, determinant
- Eigenvalues and eigenvectors
- Singular Value Decomposition (SVD)
- Least squares — solving overdetermined systems
- Positive definite matrices — what they mean for covariance

**Probability Theory**
- Random variables — discrete and continuous
- Probability density functions (PDFs)
- Joint, marginal, and conditional probability
- Law of total probability and chain rule
- Expectation, variance, covariance

**Gaussian Distributions**
- Univariate Gaussian — mean and variance
- Multivariate Gaussian — mean vector and covariance matrix
- Product of two Gaussians — the core operation behind every Kalman filter
- Marginalization and conditioning

**Bayes' Theorem**
- Prior, likelihood, posterior
- Normalization constant
- Recursive Bayesian estimation — the foundation of all state estimators

**Coordinate Transforms**
- Rotation matrices — SO(2), SO(3)
- Homogeneous coordinates
- Rigid body transforms — SE(2), SE(3)
- Composing and inverting transforms

---

## Videos

- **Cyrill Stachniss — Mobile Robotics, Lectures 1–3** (YouTube @CyrillStachniss) — probability recap and Bayes filter derivation applied directly to robotics
- **3Blue1Brown — Essence of Linear Algebra** (YouTube @3blue1brown) — 15 short videos; geometric intuition before algebra
- **3Blue1Brown — Bayes Theorem** (YouTube @3blue1brown) — single video, best visual explanation of Bayes available
- **Gilbert Strang — MIT 18.06 Linear Algebra** (MIT OCW / YouTube) — rigorous university reference; work through lectures 1–10

---

## Book / Article Resources

- **Probabilistic Robotics** — Thrun, Burgard, Fox (2005) — Chapter 2: *Recursive State Estimation*. Covers all the probability needed for this guidebook in ~40 pages.
- **State Estimation for Robotics** — Barfoot (2017) — Chapters 1–2. Rigorous treatment of Gaussian estimation and Lie group transforms.
- **Linear Algebra and Its Applications** — Gilbert Strang — textbook companion to the MIT lectures.
- **Pattern Recognition and Machine Learning** — Bishop (2006) — Chapter 2 for deeper coverage of Gaussian distributions and Bayesian methods.
