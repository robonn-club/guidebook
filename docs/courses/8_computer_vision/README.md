# Computer Vision

> Enabling robots to interpret the visual world — from geometric understanding of cameras to semantic recognition of objects, people, and scenes.

!!! info "At Bonn — MA-MORO-M04"

    Examined in **Computer Vision** (`MA-MORO-M04`), 9 CP, 1st semester — one written exam
    of 120 min (100%). Admission requires the regularly provided exercise sheets, which may
    be done in pairs, with at least 50% of the points achieved.

    This is the same module as `MA-INF 2201` in the Computer Science M.Sc., taught by
    Jürgen Gall — whose course page is linked below.

    *Sat this exam? [Tell us what it was actually like](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) — that is the part no
    module manual can give you.*

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

- **[Computer Vision (MA-INF 2201) — course page](https://pages.iai.uni-bonn.de/gall_juergen/teaching/Lectures/cv21.html)** — Jürgen Gall (Uni Bonn) — slides and materials for the Bonn computer vision lecture; the local reference for this page
- **[CS231n: Deep Learning for Computer Vision](https://www.youtube.com/playlist?list=PLC1qU-LWwrF64f4QKQT-Vg5Wr4qEE1Zxk)** — Stanford (Spring 2017) — the standard deep learning for vision course; lectures by Fei-Fei Li, Justin Johnson, and Serena Yeung
- **[Multiple View Geometry](https://www.youtube.com/playlist?list=PLTBdjV_4f-EJn6udZ34tht9EVIW7lbeo4)** — Daniel Cremers (TU München) — geometric vision; epipolar geometry, SfM, and dense reconstruction ([slides and exercises](https://vision.in.tum.de/teaching/online/mvg))
- **[First Principles of Computer Vision](https://fpcv.cs.columbia.edu/)** — Shree Nayar (Columbia) — image formation, optics, and sensing from first principles; short, tightly-scoped videos

---

## Book / Article Resources

- **[Computer Vision: Algorithms and Applications](https://szeliski.org/Book/)** — Szeliski (2nd ed., 2022) — free online; the most comprehensive single reference covering classical and modern CV
- **[Multiple View Geometry in Computer Vision](https://www.robots.ox.ac.uk/~vgg/hzbook/)** — Hartley & Zisserman (2004) — the definitive reference for geometric vision; essential for SfM and stereo
- **[An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)** — Dosovitskiy et al. (2020) — the ViT paper; short and readable; marks the shift to transformers in vision
- **[Mask R-CNN](https://arxiv.org/abs/1703.06870)** — He et al. (2017) — read alongside the Faster R-CNN paper; together they cover the detection and segmentation pipeline
- **[RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039)** — Teed & Deng (2020) — the reference formulation for learned optical flow; clean and widely built upon
