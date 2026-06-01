# Machine Learning

> Learning-based methods for robotics — from principled Bayesian regression to deep neural networks for perception and control.

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

- **Cyrill Stachniss — Gaussian Processes** (YouTube @CyrillStachniss) — full lecture series on GP regression, classification, and sparse approximations; directly applicable to robotics
- **Cyrill Stachniss — Machine Learning for Robotics** (YouTube @CyrillStachniss) — covers supervised learning, GPs, and deep learning in a robotics context
- **Andrej Karpathy — Neural Networks: Zero to Hero** (YouTube @AndrejKarpathy) — backpropagation, language models, and transformers built from scratch; best available explanation of the mechanics

---

## Book / Article Resources

- **Gaussian Processes for Machine Learning** — Rasmussen & Williams (2006) — free online at gaussianprocess.org; the reference for everything GP; chapters 2–5 cover everything listed here
- **Deep Learning** — Goodfellow, Bengio, Courville (2016) — free online; Part II (chapters 6–12) covers feedforward networks, CNNs, and optimization
- **Reinforcement Learning: An Introduction** — Sutton & Barto (2nd ed., 2018) — free online; the standard RL reference; chapters 3–6 for value methods, 13 for policy gradients
- **A Survey on Deep Learning for Robot Navigation** — Bonin-Font et al. review — good entry point for how deep learning is applied specifically in mobile robotics
