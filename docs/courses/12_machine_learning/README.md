# Machine Learning

> Learning-based methods for robotics — from principled Bayesian regression to deep neural networks for perception and control.

!!! info "At Bonn — MA-MORO-M06"

    Examined in **Machine Learning for Robotics and Computer Vision** (`MA-MORO-M06`), 6 CP,
    2nd semester — one written exam of 120 min (100%), with at least 50% of the exercise
    points required for admission. The module recommends Python and `MA-MORO-M01` beforehand.

    Its contents run past this page in places: Vision Transformers, representation learning,
    self-supervised learning and vision language models are all listed.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

---

## Topics

**Supervised Learning Foundations**
- Regression and classification — when to use each
- Loss functions — MSE, cross-entropy, and their probabilistic interpretations
- Overfitting vs. underfitting — bias-variance trade-off
- Train / validation / test splits — why the split matters; data leakage as a common mistake
- Gradient descent — batch, mini-batch, stochastic; learning rate and convergence

**Gaussian Processes**
- GP as a distribution over functions — defined by a mean function and a covariance (kernel) function
- Kernel functions — RBF (squared exponential), Matérn, periodic; kernel hyperparameters
- GP regression — closed-form posterior; predictive mean and variance give uncertainty directly
- GP classification — approximation required (Laplace, EP)
- Hyperparameter optimization — maximizing the marginal likelihood
- Applications in robotics: terrain modeling, learning motion/sensor models, active exploration
- Sparse GPs — inducing points for scaling beyond a few thousand observations

**Neural Networks**
- Feedforward networks — layers, activations (ReLU, GELU), weight initialization
- Backpropagation — chain rule through the computational graph
- CNNs — convolutional layers, pooling, receptive field; standard for image perception
- Transformers — self-attention, positional encoding; ViT for images; used in modern detection and segmentation

**Uncertainty in Learning**
- Aleatoric uncertainty — irreducible noise in the data; modeled by the output distribution
- Epistemic uncertainty — model uncertainty from limited data; reducible with more data
- Bayesian neural networks — weight distributions instead of point estimates; approximate inference
- Monte Carlo Dropout — practical uncertainty estimate; dropout at test time approximates a BNN
- Why uncertainty matters for robotics — a robot that does not know what it does not know is unsafe

**Deep Learning for Robotics Perception**
- 3D object detection from LiDAR — PointNet, PointPillars, VoxelNet
- Semantic segmentation for navigation — labeling free space, obstacles, road surface
- Imitation learning and behavior cloning — learning a policy from expert demonstrations
- Sim-to-real transfer — domain randomization, domain adaptation; why simulation alone is insufficient

**Reinforcement Learning**
- Markov Decision Process (MDP) — states, actions, rewards, transition model
- Value functions — Q-function, V-function; Bellman equation
- Q-learning and DQN — off-policy learning with a neural network function approximator
- Policy gradient methods — REINFORCE, PPO, SAC; directly optimizing the policy
- Model-based RL — learning the transition model; more sample-efficient but harder to train
- RL for robotics: reward shaping, sparse rewards, safety constraints

---

## Videos

- **[Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)** — Andrej Karpathy — backpropagation, language models, and transformers built from scratch; best available explanation of the mechanics
- **[Mobile Sensing and Robotics 2](https://www.youtube.com/playlist?list=PLgnQpQtFTOGQh_J16IMwDlji18SWQ2PZ6)** — Cyrill Stachniss (Uni Bonn) — where learned components sit inside a classical robotics stack
- **[CS231n: Deep Learning for Computer Vision](https://www.youtube.com/playlist?list=PLC1qU-LWwrF64f4QKQT-Vg5Wr4qEE1Zxk)** — Stanford — the perception half of learning for robotics, taught properly

---

## Book / Article Resources

- **[Gaussian Processes for Machine Learning](http://gaussianprocess.org/gpml/)** — Rasmussen & Williams (2006) — free online; the reference for everything GP; chapters 2–5 cover everything listed here
- **[Deep Learning](https://www.deeplearningbook.org/)** — Goodfellow, Bengio, Courville (2016) — free online; Part II (chapters 6–12) covers feedforward networks, CNNs, and optimization
- **[Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)** — Sutton & Barto (2nd ed., 2018) — free online; the standard RL reference; chapters 3–6 for value methods, 13 for policy gradients
- **[Visual Navigation for Mobile Robots: A Survey](https://doi.org/10.1007/s10846-008-9235-4)** — Bonin-Font, Ortiz, Oliver (2008) — pre-deep-learning, but the clearest taxonomy of map-based vs. mapless visual navigation; read it for the problem framing, then the modern papers for the methods
