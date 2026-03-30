# # import numpy as np
# # import cv2
# # import matplotlib.pyplot as plt
# # from scipy.optimize import least_squares

# # def normalize_points(pts, M):
# #     T = np.array([[1/M, 0, 0], [0, 1/M, 0], [0, 0, 1]])
# #     pts_hom = np.column_stack((pts, np.ones(len(pts))))
# #     pts_norm = (T @ pts_hom.T).T[:, :2]
# #     return pts_norm, T

# # def eight_point(pts1, pts2, M):
# #     pts1_norm, T1 = normalize_points(pts1, M)
# #     pts2_norm, T2 = normalize_points(pts2, M)
    
# #     A = np.column_stack([
# #         pts1_norm[:, 0] * pts2_norm[:, 0],
# #         pts1_norm[:, 0] * pts2_norm[:, 1],
# #         pts1_norm[:, 0],
# #         pts1_norm[:, 1] * pts2_norm[:, 0],
# #         pts1_norm[:, 1] * pts2_norm[:, 1],
# #         pts1_norm[:, 1],
# #         pts2_norm[:, 0],
# #         pts2_norm[:, 1],
# #         np.ones(len(pts1))
# #     ])
    
# #     _, _, Vt = np.linalg.svd(A)
# #     F = Vt[-1].reshape(3, 3)
    
# #     U, S, Vt = np.linalg.svd(F)
# #     S[-1] = 0  # Enforce rank 2 constraint
# #     F_refined = U @ np.diag(S) @ Vt
    
# #     F_final = T2.T @ F_refined @ T1
# #     return F_final

# # def rectify_pair(K1, K2, R1, R2, t1, t2):
# #     c1 = -np.linalg.inv(K1 @ R1) @ (K1 @ t1)
# #     c2 = -np.linalg.inv(K2 @ R2) @ (K2 @ t2)
    
# #     r1 = (c1 - c2) / np.linalg.norm(c1 - c2)
# #     r2 = np.cross(R1[2], r1)
# #     r2 /= np.linalg.norm(r2)
# #     r3 = np.cross(r2, r1)
# #     R_new = np.vstack((r1, r2, r3))
    
# #     R1p, R2p = R_new, R_new
# #     K1p, K2p = K2, K2
# #     t1p = -R1p @ c1
# #     t2p = -R2p @ c2
    
# #     M1 = (K1p @ R1p) @ np.linalg.inv(K1 @ R1)
# #     M2 = (K2p @ R2p) @ np.linalg.inv(K2 @ R2)
    
# #     return M1, M2, K1p, K2p, R1p, R2p, t1p, t2p

# # def disparity_map(im1, im2, max_disp, win_size):
# #     dispM = np.zeros_like(im1, dtype=np.float32)
# #     half_w = win_size // 2
    
# #     for y in range(half_w, im1.shape[0] - half_w):
# #         for x in range(half_w, im1.shape[1] - half_w):
# #             best_disp = 0
# #             min_error = float('inf')
            
# #             for d in range(max_disp):
# #                 if x - d >= 0:
# #                     error = np.sum((im1[y-half_w:y+half_w+1, x-half_w:x+half_w+1] -
# #                                     im2[y-half_w:y+half_w+1, x-d-half_w:x-d+half_w+1]) ** 2)
# #                     if error < min_error:
# #                         min_error = error
# #                         best_disp = d
            
# #             dispM[y, x] = best_disp
# #     return dispM

# # def depth_map(dispM, K1, K2, R1, R2, t1, t2):
# #     b = np.linalg.norm(-np.linalg.inv(K1 @ R1) @ (K1 @ t1) - (-np.linalg.inv(K2 @ R2) @ (K2 @ t2)))
# #     f = K1[0, 0]
# #     depthM = np.where(dispM > 0, b * f / dispM, 0)
# #     return depthM

# # def run_pipeline():
# #     data = np.load("intrinsics.npz")
# #     K1, K2 = data["K1"], data["K2"]
    
# #     im1 = cv2.imread("data/im1.png", cv2.IMREAD_GRAYSCALE)
# #     im2 = cv2.imread("data/im2.png", cv2.IMREAD_GRAYSCALE)
    
# #     M = max(im1.shape)
# #     data_pts = np.load("some_corresp.npz")
# #     pts1, pts2 = data_pts["pts1"], data_pts["pts2"]
    
# #     F = eight_point(pts1, pts2, M)
# #     print("Fundamental Matrix:", F)
    
# #     extrinsics = np.load("extrinsics.npz")######################################
# #     R1, R2, t1, t2 = extrinsics["R1"], extrinsics["R2"], extrinsics["t1"], extrinsics["t2"]
    
# #     M1, M2, K1p, K2p, R1p, R2p, t1p, t2p = rectify_pair(K1, K2, R1, R2, t1, t2)
    
# #     dispM = disparity_map(im1, im2, max_disp=64, win_size=9)
# #     plt.imshow(dispM, cmap='jet')
# #     plt.title("Disparity Map")
# #     plt.colorbar()
# #     plt.show()
    
# #     depthM = depth_map(dispM, K1, K2, R1, R2, t1, t2)
# #     plt.imshow(depthM, cmap='jet')
# #     plt.title("Depth Map")
# #     plt.colorbar()
# #     plt.show()

# # if __name__ == "__main__":
# #     run_pipeline()


# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
# from scipy.optimize import least_squares

# def normalize_points(pts, M):
#     T = np.array([[1/M, 0, 0], [0, 1/M, 0], [0, 0, 1]])
#     pts_hom = np.column_stack((pts, np.ones(len(pts))))
#     pts_norm = (T @ pts_hom.T).T[:, :2]
#     return pts_norm, T

# def eight_point(pts1, pts2, M):
#     pts1_norm, T1 = normalize_points(pts1, M)
#     pts2_norm, T2 = normalize_points(pts2, M)
    
#     A = np.column_stack([
#         pts1_norm[:, 0] * pts2_norm[:, 0],
#         pts1_norm[:, 0] * pts2_norm[:, 1],
#         pts1_norm[:, 0],
#         pts1_norm[:, 1] * pts2_norm[:, 0],
#         pts1_norm[:, 1] * pts2_norm[:, 1],
#         pts1_norm[:, 1],
#         pts2_norm[:, 0],
#         pts2_norm[:, 1],
#         np.ones(len(pts1))
#     ])
    
#     _, _, Vt = np.linalg.svd(A)
#     F = Vt[-1].reshape(3, 3)
    
#     U, S, Vt = np.linalg.svd(F)
#     S[-1] = 0  # Enforce rank 2 constraint
#     F_refined = U @ np.diag(S) @ Vt
    
#     F_final = T2.T @ F_refined @ T1
#     return F_final

# def essential_matrix(F, K1, K2):
#     return K2.T @ F @ K1

# def extract_extrinsics(E):
#     U, S, Vt = np.linalg.svd(E)
#     if np.linalg.det(U @ Vt) < 0:
#         Vt = -Vt
#     R1 = U @ np.diag([1, 1, 1]) @ Vt
#     R2 = U @ np.diag([1, 1, -1]) @ Vt
#     t = U[:, 2]
#     return (R1, t), (R1, -t), (R2, t), (R2, -t)

# def select_correct_extrinsics(R_t_candidates, K1, pts1, K2, pts2):
#     P1 = K1 @ np.hstack((np.eye(3), np.zeros((3, 1))))
#     best_count = 0
#     best_R, best_t = None, None
#     for R, t in R_t_candidates:
#         P2 = K2 @ np.hstack((R, t.reshape(-1, 1)))
#         pts3d = triangulate(P1, pts1, P2, pts2)
#         num_positive_depth = np.sum(pts3d[:, 2] > 0)
#         if num_positive_depth > best_count:
#             best_count = num_positive_depth
#             best_R, best_t = R, t
#     return best_R, best_t

# def triangulate(P1, pts1, P2, pts2):
#     pts3d = []
#     for i in range(len(pts1)):
#         A = np.array([
#             pts1[i, 0] * P1[2, :] - P1[0, :],
#             pts1[i, 1] * P1[2, :] - P1[1, :],
#             pts2[i, 0] * P2[2, :] - P2[0, :],
#             pts2[i, 1] * P2[2, :] - P2[1, :]
#         ])
#         _, _, Vt = np.linalg.svd(A)
#         X = Vt[-1]
#         X /= X[3]
#         pts3d.append(X[:3])
#     return np.array(pts3d)

# def run_pipeline():
#     data = np.load("data/intrinsics.npz")
#     K1, K2 = data["K1"], data["K2"]
    
#     im1 = cv2.imread("data/im1.png", cv2.IMREAD_GRAYSCALE)
#     im2 = cv2.imread("data/im2.png", cv2.IMREAD_GRAYSCALE)
    
#     M = max(im1.shape)
#     data_pts = np.load("data/some_corresp.npz")
#     pts1, pts2 = data_pts["pts1"], data_pts["pts2"]
    
#     F = eight_point(pts1, pts2, M)
#     print("Fundamental Matrix:", F)
    
#     E = essential_matrix(F, K1, K2)
#     print("Essential Matrix:", E)
    
#     R_t_candidates = extract_extrinsics(E)
#     R, t = select_correct_extrinsics(R_t_candidates, K1, pts1, K2, pts2)
    
#     np.savez("data/extrinsics.npz", R1=R, R2=R, t1=t, t2=-t)
#     print("Extrinsic Parameters Saved")
    
# if __name__ == "__main__":
#     run_pipeline()



import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

def normalize_points(pts, M):
    T = np.array([[1/M, 0, 0], [0, 1/M, 0], [0, 0, 1]])
    pts_hom = np.column_stack((pts, np.ones(len(pts))))
    pts_norm = (T @ pts_hom.T).T[:, :2]
    return pts_norm, T

def eight_point(pts1, pts2, M):
    pts1_norm, T1 = normalize_points(pts1, M)
    pts2_norm, T2 = normalize_points(pts2, M)
    
    A = np.column_stack([
        pts1_norm[:, 0] * pts2_norm[:, 0],
        pts1_norm[:, 0] * pts2_norm[:, 1],
        pts1_norm[:, 0],
        pts1_norm[:, 1] * pts2_norm[:, 0],
        pts1_norm[:, 1] * pts2_norm[:, 1],
        pts1_norm[:, 1],
        pts2_norm[:, 0],
        pts2_norm[:, 1],
        np.ones(len(pts1))
    ])
    
    _, _, Vt = np.linalg.svd(A)
    F = Vt[-1].reshape(3, 3)
    
    U, S, Vt = np.linalg.svd(F)
    S[-1] = 0  # Enforce rank 2 constraint
    F_refined = U @ np.diag(S) @ Vt
    
    F_final = T2.T @ F_refined @ T1
    return F_final

def essential_matrix(F, K1, K2):
    return K2.T @ F @ K1

# def epipolar_correspondences(im1, im2, F, pts1):
#     pts2 = []
#     for (x1, y1) in pts1:
#         epiline = F @ np.array([x1, y1, 1])
#         a, b, c = epiline
#         min_error = float('inf')
#         best_match = None
#         for x2 in range(im2.shape[1]):
#             y2 = int((-a * x2 - c) / b) if b != 0 else y1
#             if 0 <= y2 < im2.shape[0]:
#                 error = np.sum((im1[y1-3:y1+3, x1-3:x1+3] - im2[y2-3:y2+3, x2-3:x2+3]) ** 2)
#                 if error < min_error:
#                     min_error = error
#                     best_match = (x2, y2)
#         if best_match:
#             pts2.append(best_match)
#     return np.array(pts2)

def epipolar_correspondences(im1, im2, F, pts1):
    h1, w1 = im1.shape
    h2, w2 = im2.shape
    pts2 = []

    for (x1, y1) in pts1:
        epiline = F @ np.array([x1, y1, 1])
        a, b, c = epiline
        min_error = float('inf')
        best_match = None

        for x2 in range(w2):
            if b == 0:  # Avoid division by zero
                continue
            y2 = int((-a * x2 - c) / b)
            
            if 3 <= x2 < w2 - 3 and 3 <= y2 < h2 - 3 and 3 <= x1 < w1 - 3 and 3 <= y1 < h1 - 3:
                patch1 = im1[y1-3:y1+3, x1-3:x1+3]
                patch2 = im2[y2-3:y2+3, x2-3:x2+3]

                if patch1.shape == patch2.shape:  # Ensure both patches are valid
                    error = np.sum((patch1 - patch2) ** 2)
                    if error < min_error:
                        min_error = error
                        best_match = (x2, y2)

        if best_match:
            pts2.append(best_match)

    return np.array(pts2)


def extract_extrinsics(E):
    U, S, Vt = np.linalg.svd(E)
    if np.linalg.det(U @ Vt) < 0:
        Vt = -Vt
    R1 = U @ np.diag([1, 1, 1]) @ Vt
    R2 = U @ np.diag([1, 1, -1]) @ Vt
    t = U[:, 2]
    return (R1, t), (R1, -t), (R2, t), (R2, -t)

def select_correct_extrinsics(R_t_candidates, K1, pts1, K2, pts2):
    P1 = K1 @ np.hstack((np.eye(3), np.zeros((3, 1))))
    best_count = 0
    best_R, best_t = None, None
    for R, t in R_t_candidates:
        P2 = K2 @ np.hstack((R, t.reshape(-1, 1)))
        pts3d = triangulate(P1, pts1, P2, pts2)
        num_positive_depth = np.sum(pts3d[:, 2] > 0)
        if num_positive_depth > best_count:
            best_count = num_positive_depth
            best_R, best_t = R, t
    return best_R, best_t

def triangulate(P1, pts1, P2, pts2):
    pts3d = []
    for i in range(len(pts1)):
        A = np.array([
            pts1[i, 0] * P1[2, :] - P1[0, :],
            pts1[i, 1] * P1[2, :] - P1[1, :],
            pts2[i, 0] * P2[2, :] - P2[0, :],
            pts2[i, 1] * P2[2, :] - P2[1, :]
        ])
        _, _, Vt = np.linalg.svd(A)
        X = Vt[-1]
        X /= X[3]
        pts3d.append(X[:3])
    return np.array(pts3d)



def plot_3d_points(pts3d):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pts3d[:, 0], pts3d[:, 1], pts3d[:, 2], marker='o', s=1)
    ax.set_xlabel('X -> horizontal spatial position')
    ax.set_ylabel('Y -> vertical spatial position')
    ax.set_zlabel('Z -> depth')
    ax.set_title('3D Reconstruction')
    plt.show()


def run_temple_reconstruction():
    data = np.load("Input_Data/intrinsics.npz")
    K1, K2 = data["K1"], data["K2"]
    
    im1 = cv2.imread("Input_Data/im1.png", cv2.IMREAD_GRAYSCALE)
    im2 = cv2.imread("Input_Data/im2.png", cv2.IMREAD_GRAYSCALE)
    
    M = max(im1.shape)
    data_pts = np.load("Input_Data/some_corresp.npz")
    pts1, pts2 = data_pts["pts1"], data_pts["pts2"]
    
    F = eight_point(pts1, pts2, M)
    print("Fundamental Matrix:", F)
    
    temple_coords = np.load("Input_Data/temple_coords.npz")
    temple_pts1 = temple_coords["pts1"]
    temple_pts2 = epipolar_correspondences(im1, im2, F, temple_pts1)
    
    E = essential_matrix(F, K1, K2)
    print("Essential Matrix:", E)
    R_t_candidates = extract_extrinsics(E)
    R, t = select_correct_extrinsics(R_t_candidates, K1, pts1, K2, pts2)
    
    np.savez("Input_Data/extrinsics.npz", R1=R, R2=R, t1=t, t2=-t)
    
    P1 = K1 @ np.hstack((np.eye(3), np.zeros((3, 1))))
    P2 = K2 @ np.hstack((R, t.reshape(-1, 1)))
    
    pts3d = triangulate(P1, temple_pts1, P2, temple_pts2)
    plot_3d_points(pts3d)
    
if __name__ == "__main__":
    run_temple_reconstruction()
