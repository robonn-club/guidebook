# Computer Vision

> Enabling robots to interpret the visual world — from geometric understanding of cameras to semantic recognition of objects, people, and scenes.

---

## Topics

**Camera Models and Calibration**
- Pinhole camera model — intrinsic matrix K, focal length, principal point
- Lens distortion — radial and tangential coefficients; correcting with OpenCV
- Stereo camera geometry — baseline, disparity, depth from triangulation
- Wide-angle and fisheye models — important for automotive and drone platforms
- Calibration — checkerboard method, Zhang's algorithm, reprojection error

**Image Formation and Classical Features**
- Image pyramids and scale-space — why SIFT is scale-invariant
- Harris corner detector — second moment matrix, cornerness score
- SIFT — scale and rotation invariant descriptor; still used in SfM pipelines
- ORB — binary descriptor; fast enough for real-time SLAM
- Histogram of Oriented Gradients (HOG) — dense descriptor; baseline for detection
- Feature matching — brute-force, FLANN, ratio test (Lowe's criterion)

**Geometric Vision**
- Homography — mapping between planes; used for camera pose from planar scenes
- Epipolar geometry — fundamental matrix F, essential matrix E
- Stereo reconstruction — disparity map to depth, semi-global matching (SGM)
- PnP problem — estimating camera pose from 2D-3D correspondences; the core of visual SLAM localization
- Structure from Motion (SfM) — incremental reconstruction; bundle adjustment as the back-end
- Bundle adjustment — joint optimization of camera poses and 3D points; sparse Levenberg-Marquardt

**Deep Learning for Visual Perception**
- CNN architectures — AlexNet → VGG → ResNet → EfficientNet; what changed and why
- Object detection — Faster R-CNN (two-stage), YOLO (one-stage); speed vs. accuracy trade-off
- Semantic segmentation — FCN, DeepLab, SegNet; assigning class labels to every pixel; essential for robot navigation and obstacle avoidance
- Instance segmentation — Mask R-CNN; separate mask per object instance
- Vision Transformers — ViT, Swin Transformer; patch-based attention replacing convolutions
- DETR — end-to-end object detection with transformers; no NMS required
- Monocular depth estimation — MiDaS, DPT; metric vs. relative depth

**2D and 3D Pose Estimation**
- 2D human pose estimation — heatmap regression; HRNet, ViTPose
- 6-DoF object pose estimation — estimating position and orientation of objects; critical for robotic manipulation
- Pose estimation in the wild — occlusion handling, multi-person scenarios

**Temporal Modeling and Video**
- Optical flow — Lucas-Kanade (sparse), Horn-Schunck (dense), RAFT (learning-based)
- The aperture problem — why local flow estimates are ambiguous; global methods resolve it
- Object tracking — SORT (Kalman + Hungarian), DeepSORT (appearance features), ByteTrack
- Action recognition — two-stream networks (spatial + temporal), I3D, SlowFast networks
- Video object segmentation — propagating masks through time

---

## Videos

- **Jürgen Gall — Computer Vision lecture series** (YouTube, Universität Bonn) — covers classical and deep learning CV with robotics applications; primary reference for this page
- **CS231n — Deep Learning for Computer Vision** (Stanford, YouTube) — the standard deep learning for vision course; lectures by Fei-Fei Li and Andrej Karpathy
- **Daniel Cremers — Multiple View Geometry** (YouTube @DanielCremers4) — geometric vision; epipolar geometry, SfM, and dense reconstruction
- **First Principles of Computer Vision** (YouTube, Columbia / Shree Nayar) — image formation, optics, and sensing from first principles

---

## Book / Article Resources

- **Computer Vision: Algorithms and Applications** — Szeliski (2nd ed., 2022) — free online; the most comprehensive single reference covering classical and modern CV
- **Multiple View Geometry in Computer Vision** — Hartley & Zisserman (2004) — the definitive reference for geometric vision; essential for SfM and stereo
- **An Image is Worth 16x16 Words** — Dosovitskiy et al. (2020) — the ViT paper; short and readable; marks the shift to transformers in vision
- **Mask R-CNN** — He et al. (2017) — read alongside the Faster R-CNN paper; together they cover the detection and segmentation pipeline
- **RAFT: Recurrent All-Pairs Field Transforms for Optical Flow** — Teed & Deng (2020) — current state of the art in optical flow; clean formulation
