# AGV Task Solutions

This repository contains solutions for selected tasks as part of the AGV (Autonomous Ground Vehicle) tasks.

## Project Overview

This project involves implementing software solutions for controlling and managing AGVs. The tasks focus on various aspects of AGV operation, including navigation, task management, and system integration.


## Implemented Tasks

This repository provides solutions for the following tasks:

*   Task 1
*   Task 5
*   Task 6

---

## TASK 1: Optical Flow

### Problem Statement (Subtask 1: CJ NEEDS HELP!: IMPLEMENTING OPTICAL FLOW)

You are expected to implement the Lucas-Kanade sparse optical flow estimation algorithm specified in this article (https://nanonets.com/blog/optical-flow/) on clips of your choice from this video. You are allowed to use basic OpenCV functions: cv2.imread, cv2.imshow, etc., and you may additionally use cv2.goodFeaturesToTrack. You may refer OpenCV documentation.


### Solution

The solution for Task 1 is implemented in `TASK_1/mainCode.py`. It utilizes the Lucas-Kanade sparse optical flow algorithm to detect and visualize motion vectors between consecutive frames of an input video.

Key features:
- Detects strong corners in the initial frame to track.
- Calculates optical flow to track these corners in subsequent frames.
- Visualizes the motion vectors (lines) on the video frames, showing the direction and magnitude of movement.
- Displays the processed video with motion vectors in real-time.

### Input Video

The script uses the following video file as input:
`TASK_1/Input_Video_Task_1/OPTICAL_FLOW.mp4`

### How to Run

1.  Ensure you have Python installed along with the necessary libraries (OpenCV, NumPy).
2.  Navigate to the repository's root directory.
3.  Run the script using the following command:
    ```bash
    python TASK_1/mainCode.py
    ```

---

## TASK 5: Localization with Correlative Scan Matching

### Problem Statement

Task: Correlative Scan Matching for Localization. The task involves reading and implementing the research paper titled “A 2D-LiDAR- based localization method for indoor mobile robots using correlative scan matching” by Song Du, Tao Chen, Zhonghui Lou, and Yijie Wu (https://www.cambridge.org/core/journals/robotica/article/abs/2dlidarbased-localization-method-for-indoor-mobile-robots-using-correlative-scan-matching/291583763D866B1739AEF58ADC34D659). You will have to implement the localization method using the correlative scan matching (CSM) technique on this dataset (http://ais.informatik.uni-freiburg.de/slamevaluation/datasets/aces.clf).

SUBTASK 1: Use the dataset above with the noise parameters of your choice to localize the agent on this map (use OpenCV to replace green pixels with white ones).

SUBTASK 2: Utilize this solution to estimate better noise parameters and provide your rationale for doing so.

### Solution

The solution for Task 5 is implemented in `TASK_5/mainCode.py`. This script performs localization of a robot using 2D LiDAR data and a map via the Correlative Scan Matching (CSM) technique.

Key features:
- Loads a map image (`map.png`) and preprocesses it (e.g., converting green pixels to white, converting to grayscale, and applying thresholding). The processed map is saved as `processed_map.png`.
- Loads LiDAR scan data from `aces.clf.txt`. Each line in this file typically represents a series of range measurements from the LiDAR.
- Implements the Correlative Scan Matching algorithm to find the best match between the LiDAR scans and the map, thereby estimating the robot's position (x, y) and orientation (theta) on the map.
- Outputs the estimated position and orientation to the console.

### Inputs

-   Map file: `TASK_5/map.png`
-   LiDAR data file: `TASK_5/aces.clf.txt`

### Outputs

-   Processed map image: `TASK_5/processed_map.png`
-   Console output: Estimated position (x, y) and orientation (theta) of the robot.

### How to Run

1.  Ensure you have Python installed along with the necessary libraries (e.g., OpenCV, NumPy).
2.  Navigate to the repository's root directory.
3.  Run the script using the following command:
    ```bash
    python TASK_5/mainCode.py
    ```

---

## TASK 6: 3D Reconstruction

### Problem Statement

Task: This task requires you to construct 3D representation of surroundings from multiple view images. A detailed description of the concept behind the task and how you are expected to tackle it are given in the Link. All the required data is also given in the link (https://drive.google.com/drive/folders/1orQVS0M1EvUs7I_R0d2-KAedNLS0zhIk).

### Solution

This task is divided into two parts, implemented in two separate Python scripts.

**Part 1: Epipolar Geometry and 3D Point Cloud Generation (`TASK_6/task-6.py`)**

This script focuses on estimating the camera extrinsics and triangulating 3D points from two images of the "temple" dataset.

Key features:
- Loads two images (`im1.png`, `im2.png`), intrinsic camera parameters (`intrinsics.npz`), and some initial point correspondences (`some_corresp.npz`).
- Calculates the Fundamental matrix (F) from the correspondences.
- Calculates the Essential matrix (E) using the intrinsic parameters and F.
- Recovers the relative Rotation (R) and translation (t) between the two camera views from E. The script selects the correct R and t from possible solutions.
- Finds more point correspondences between the two images.
- Triangulates the 3D coordinates of these corresponding points.
- Visualizes the epipolar lines on the images and plots the reconstructed 3D point cloud of the temple.
- Saves the computed extrinsics (R, t) to `Input_Data/extrinsics.npz`.

**Part 2: Stereo Rectification, Disparity and Depth Maps (`TASK_6/task-6_part-2.py`)**

This script focuses on stereo rectification and computing disparity and depth maps from the two "temple" images.

Key features:
- Loads the images, intrinsic parameters, and the extrinsics computed in Part 1 (`Input_Data/extrinsics.npz`).
- Performs stereo rectification on the two images to make their epipolar lines horizontal and parallel.
- Computes the disparity map between the rectified images, which represents the difference in horizontal coordinates of corresponding pixels.
- Computes the depth map from the disparity map, which provides an estimate of the distance of each point from the camera.
- Visualizes the rectified images, the disparity map, and the depth map.
- Saves the rectification parameters to `Input_Data/rectify.npz` and the depth map results to `Input_Data/depth_results.npz`.

### Inputs

The scripts use the following input files located in the `TASK_6/Input_Data/` directory:
-   `im1.png`: First image of the temple.
-   `im2.png`: Second image of the temple.
-   `intrinsics.npz`: Camera intrinsic parameters (e.g., focal length, principal point).
-   `some_corresp.npz`: A small set of manually selected point correspondences between `im1.png` and `im2.png`. Used for initial F matrix estimation in `task-6.py`.
-   `temple_coords.npz`: Contains coordinates for a more dense set of points used in `task-6.py` for finding more correspondences.
-   `extrinsics.npz` (generated by `task-6.py`, used by `task-6_part-2.py`): Contains the rotation and translation matrices describing the relative pose of the second camera with respect to the first.


### Outputs

**`TASK_6/task-6.py`:**
-   `TASK_6/Input_Data/extrinsics.npz`: Saved NumPy archive containing the calculated rotation (R) and translation (t) matrices.
-   Plots: Visualizations of epipolar lines and the 3D reconstructed point cloud of the temple.

**`TASK_6/task-6_part-2.py`:**
-   `TASK_6/Input_Data/rectify.npz`: Saved NumPy archive containing rectification parameters.
-   `TASK_6/Input_Data/depth_results.npz`: Saved NumPy archive containing the disparity and depth maps.
-   Plots: Visualizations of the rectified images, disparity map, and depth map.

### How to Run

1.  Ensure you have Python installed along with the necessary libraries (e.g., OpenCV, NumPy, Matplotlib).
2.  Navigate to the repository's root directory.
3.  Run the scripts sequentially:

    First, run `task-6.py` to compute extrinsics and generate the 3D point cloud:
    ```bash
    python TASK_6/task-6.py
    ```

    Then, run `task-6_part-2.py` to perform stereo rectification and generate disparity/depth maps:
    ```bash
    python TASK_6/task-6_part-2.py
    ```
