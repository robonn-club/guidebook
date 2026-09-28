# Math & Probability

> The two languages of mobile robotics — linear algebra to represent the world, probability theory to represent uncertainty about it.

!!! warning "At Bonn — not taught, but assumed"

    **No mandatory MoRo module covers this material.** `MA-MORO-M04` (Computer Vision)
    lists "basic knowledge of linear algebra, analysis, probability theory" as recommended
    background, and `MA-MORO-M01` recommends basic Python for its homework. If you arrive
    without this, nobody is going to teach it to you — this page is the catch-up list.

    *Caught up on this after arriving? [Tell us what worked](https://github.com/robonn-club/guidebook/issues/new?template=suggest-resource.yml).*

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

- **[Mobile Sensing and Robotics 1 — Lectures 1–3](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQEn33QDVGJpiZLi-SlL7vA)** — Cyrill Stachniss (Uni Bonn) — probability recap and Bayes filter derivation applied directly to robotics
- **[Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)** — 3Blue1Brown — 15 short videos; geometric intuition before algebra
- **[Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM)** — 3Blue1Brown — single video, best visual explanation of Bayes available
- **[MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)** — Gilbert Strang (MIT OpenCourseWare) — rigorous university reference; work through lectures 1–10

---

## Book / Article Resources

- **[Probabilistic Robotics](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)** — Thrun, Burgard, Fox (2005) — Chapter 2: *Recursive State Estimation*. Covers all the probability needed for this guidebook in ~40 pages.
- **[State Estimation for Robotics](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser17.pdf)** — Barfoot (2017) — Chapters 1–2. Rigorous treatment of Gaussian estimation and Lie group transforms. Free PDF from the author.
- **[Linear Algebra and Its Applications](https://math.mit.edu/~gs/linearalgebra/)** — Gilbert Strang — textbook companion to the MIT lectures.
- **[Pattern Recognition and Machine Learning](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/)** — Bishop (2006) — Chapter 2 for deeper coverage of Gaussian distributions and Bayesian methods. Free PDF from Microsoft Research.
