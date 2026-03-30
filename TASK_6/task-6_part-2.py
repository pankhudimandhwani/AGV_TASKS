# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.linalg import svd
# from scipy.signal import convolve2d
# import cv2

# def rectify_pair(K1, K2, R1, R2, t1, t2):
#     # Compute optical centers
#     c1 = -np.linalg.inv(K1 @ R1) @ (K1 @ t1)
#     c2 = -np.linalg.inv(K2 @ R2) @ (K2 @ t2)
    
#     # Compute the new rotation matrix
#     r1 = (c1 - c2) / np.linalg.norm(c1 - c2)  # Baseline direction
#     r2 = np.cross(R1[2, :], r1)  # Orthonormal y-axis
#     r2 /= np.linalg.norm(r2)
#     r3 = np.cross(r1, r2)  # Orthonormal z-axis
#     R_new = np.vstack((r1, r2, r3))
    
#     # Compute new camera parameters
#     R1p = R_new
#     R2p = R_new
#     K1p = K1
#     K2p = K2
#     t1p = -R_new @ c1
#     t2p = -R_new @ c2
    
#     # Compute rectification matrices
#     M1 = (K1p @ R1p) @ np.linalg.inv(K1 @ R1)
#     M2 = (K2p @ R2p) @ np.linalg.inv(K2 @ R2)
    
#     return M1, M2, K1p, K2p, R1p, R2p, t1p, t2p

# def get_disparity(im1, im2, max_disp, win_size):
#     h = im1.shape[0]
#     w = im1.shape[1]
#     disparity_map = np.zeros((h, w))
#     half_win = win_size // 2
    
#     for y in range(half_win, h - half_win):
#         for x in range(half_win, w - half_win):
#             best_offset = 0
#             best_score = float('inf')
            
#             for d in range(min(max_disp, x)):
#                 left_patch = im1[y-half_win:y+half_win+1, x-half_win:x+half_win+1]
#                 right_patch = im2[y-half_win:y+half_win+1, x-half_win-d:x+half_win+1-d]
                
#                 if right_patch.shape != left_patch.shape:
#                     continue
                
#                 score = np.sum((left_patch - right_patch) ** 2)
#                 if score < best_score:
#                     best_score = score
#                     best_offset = d
            
#             disparity_map[y, x] = best_offset
    
#     return disparity_map

# def get_depth(disparity_map, K1, K2, R1, R2, t1, t2):
#     baseline = np.linalg.norm(-np.linalg.inv(K1 @ R1) @ (K1 @ t1) - (-np.linalg.inv(K2 @ R2) @ (K2 @ t2)))
#     focal_length = K1[0, 0]
    
#     depth_map = np.zeros_like(disparity_map)
#     valid_disp = disparity_map > 0
#     depth_map[valid_disp] = (baseline * focal_length) / disparity_map[valid_disp]
    
#     return depth_map

# # def draw_epipolar_lines(image, num_lines=10):
# #     h, w = image.shape
# #     step = h // num_lines
# #     for i in range(0, h, step):
# #         cv2.line(image, (0, i), (w, i), (255, 0, 0), 1)
# #     return image

# # # Load rectified images and draw epipolar lines
# # rectified_im1 = draw_epipolar_lines(im1.copy())
# # rectified_im2 = draw_epipolar_lines(im2.copy())

# # Display rectified images with epipolar lines
# # plt.figure(figsize=(10, 5))
# # plt.subplot(1, 2, 1)
# # plt.imshow(rectified_im1, cmap="gray")
# # plt.title("Rectified Image 1 with Epipolar Lines")

# # plt.subplot(1, 2, 2)
# # plt.imshow(rectified_im2, cmap="gray")
# # plt.title("Rectified Image 2 with Epipolar Lines")

# # plt.show()


# def main():
#     # Load intrinsic and extrinsic parameters
#     intrinsics = np.load("data/intrinsics.npz")
#     extrinsics = np.load("data/extrinsics.npz")
#     K1, K2 = intrinsics['K1'], intrinsics['K2']
#     R1, R2, t1, t2 = extrinsics['R1'], extrinsics['R2'], extrinsics['t1'], extrinsics['t2']
    
#     # Compute rectification
#     M1, M2, K1p, K2p, R1p, R2p, t1p, t2p = rectify_pair(K1, K2, R1, R2, t1, t2)
    
#     # Load stereo images (convert to grayscale)
#     im1 = cv2.imread("data/im1.png", cv2.IMREAD_GRAYSCALE)
#     im2 = cv2.imread("data/im2.png", cv2.IMREAD_GRAYSCALE)
    
#     # h, w = im1.shape
#     # im1_rectified = cv2.warpPerspective(im1, M1, (w, h))
#     # im2_rectified = cv2.warpPerspective(im2, M2, (w, h))

#     # # Draw epipolar lines on rectified images
#     # im1_with_lines = draw_epipolar_lines(im1_rectified.copy())
#     # im2_with_lines = draw_epipolar_lines(im2_rectified.copy())

#     # # Display rectified images with epipolar lines
#     # plt.figure(figsize=(10, 5))
#     # plt.subplot(1, 2, 1)
#     # plt.imshow(im1_with_lines, cmap="gray")
#     # plt.title("Rectified Image 1 with Epipolar Lines")

#     # plt.subplot(1, 2, 2)
#     # plt.imshow(im2_with_lines, cmap="gray")
#     # plt.title("Rectified Image 2 with Epipolar Lines")

#     # plt.show()

#     # Compute disparity map
#     dispM = get_disparity(im1, im2, max_disp=64, win_size=5)
    
#     # Compute depth map
#     depthM = get_depth(dispM, K1, K2, R1, R2, t1, t2)
    
#     # Save results
#     np.savez("data/rectify.npz", M1=M1, M2=M2, K1p=K1p, K2p=K2p, R1p=R1p, R2p=R2p, t1p=t1p, t2p=t2p)
#     np.savez("data/depth_results.npz", disparity=dispM, depth=depthM)

#     # Display disparity and depth maps
#     plt.figure(figsize=(10, 5))
#     plt.subplot(1, 2, 1)
#     plt.imshow(dispM, cmap="plasma")
#     plt.colorbar()
#     plt.title("Disparity Map")
    
#     plt.subplot(1, 2, 2)
#     plt.imshow(depthM, cmap="viridis")
#     plt.colorbar()
#     plt.title("Depth Map")
    
#     plt.show()

# if __name__ == "__main__":
#     main()



import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd
from scipy.signal import convolve2d
import cv2

def rectify_pair(K1, K2, R1, R2, t1, t2):
    # Compute optical centers
    c1 = -np.linalg.inv(K1 @ R1) @ (K1 @ t1)
    c2 = -np.linalg.inv(K2 @ R2) @ (K2 @ t2)
    
    # Compute the new rotation matrix
    r1 = (c1 - c2) / np.linalg.norm(c1 - c2)  # Baseline direction
    r2 = np.cross(R1[2, :], r1)  # Orthonormal y-axis
    r2 /= np.linalg.norm(r2)
    r3 = np.cross(r1, r2)  # Orthonormal z-axis
    R_new = np.vstack((r1, r2, r3))
    
    # Compute new camera parameters
    R1p = R_new
    R2p = R_new
    K1p = K1
    K2p = K2
    t1p = -R_new @ c1
    t2p = -R_new @ c2
    
    # Compute rectification matrices
    M1 = (K1p @ R1p) @ np.linalg.inv(K1 @ R1)
    M2 = (K2p @ R2p) @ np.linalg.inv(K2 @ R2)
    
    return M1, M2, K1p, K2p, R1p, R2p, t1p, t2p

def get_disparity(im1, im2, max_disp, win_size):
    h = im1.shape[0]
    w = im1.shape[1]
    disparity_map = np.zeros((h, w))
    half_win = win_size // 2
    
    for y in range(half_win, h - half_win):
        for x in range(half_win, w - half_win):
            best_offset = 0
            best_score = float('inf')
            
            for d in range(min(max_disp, x)):
                left_patch = im1[y-half_win:y+half_win+1, x-half_win:x+half_win+1]
                right_patch = im2[y-half_win:y+half_win+1, x-half_win-d:x+half_win+1-d]
                
                if right_patch.shape != left_patch.shape:
                    continue
                
                score = np.sum((left_patch - right_patch) ** 2)
                if score < best_score:
                    best_score = score
                    best_offset = d
            
            disparity_map[y, x] = best_offset
    
    return disparity_map

def get_depth(disparity_map, K1, K2, R1, R2, t1, t2):
    baseline = np.linalg.norm(-np.linalg.inv(K1 @ R1) @ (K1 @ t1) - (-np.linalg.inv(K2 @ R2) @ (K2 @ t2)))
    focal_length = K1[0, 0]
    
    depth_map = np.zeros_like(disparity_map)
    valid_disp = disparity_map > 0
    depth_map[valid_disp] = (baseline * focal_length) / disparity_map[valid_disp]
    
    return depth_map

def main():
    # Load intrinsic and extrinsic parameters
    intrinsics = np.load("Input_Data/intrinsics.npz")
    extrinsics = np.load("Input_Data/extrinsics.npz")
    K1, K2 = intrinsics['K1'], intrinsics['K2']
    R1, R2, t1, t2 = extrinsics['R1'], extrinsics['R2'], extrinsics['t1'], extrinsics['t2']
    
    # Compute rectification
    M1, M2, K1p, K2p, R1p, R2p, t1p, t2p = rectify_pair(K1, K2, R1, R2, t1, t2)
    
    # Load stereo images (convert to grayscale)
    im1 = cv2.imread("Input_Data/im1.png", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Input_Data/im2.png", cv2.IMREAD_GRAYSCALE)
    
    # Compute disparity map
    dispM = get_disparity(im1, im2, max_disp=64, win_size=5)
    
    # Compute depth map
    depthM = get_depth(dispM, K1, K2, R1, R2, t1, t2)
    
    # Save results
    np.savez("Input_Data/rectify.npz", M1=M1, M2=M2, K1p=K1p, K2p=K2p, R1p=R1p, R2p=R2p, t1p=t1p, t2p=t2p)
    np.savez("Input_Data/depth_results.npz", disparity=dispM, depth=depthM)

    # Display disparity and depth maps
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(dispM, cmap="plasma")
    plt.colorbar()
    plt.title("Disparity Map")
    
    plt.subplot(1, 2, 2)
    plt.imshow(depthM, cmap="viridis")
    plt.colorbar()
    plt.title("Depth Map")
    
    plt.show()

if __name__ == "__main__":
    main()