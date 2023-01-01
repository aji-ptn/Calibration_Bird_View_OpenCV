import cv2

# assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob

CHECKERBOARD = (6, 8)
subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.1)
# calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_FIX_SKEW  # https://stackoverflow.com/questions/49038464/opencv-calibrate-fisheye-lens-error-ill-conditioned-matrix
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
_img_shape = None
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
# images = glob.glob('/home/aji/Documents/MyGithub/create-dataset-birds-view/images/entaniya_1_more/*.jpg')
# images = glob.glob('/home/aji/Documents/MyGithub/OpenCV_bird_view_main/calibration/images/*.jpg')
images = glob.glob('/home/aji/Documents/MyGithub/OpenCV_bird_view_main/calibration/images/cam_13/*.jpg')
print(images)

for fname in images:
    img = cv2.imread(fname)
    if _img_shape is None:
        _img_shape = img.shape[:2]
    else:
        assert _img_shape == img.shape[:2], "All images must share the same size."
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    # If found, add object points, image points (after refining them)
    i = 1
    if ret:
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (6, 8), corners, ret)
        img_resize = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)), cv2.INTER_AREA)
        # cv2.imwrite("/home/aji/Documents/MyGithub/create-dataset-birds-view/images/entaniya_1/" + str(i) + ".png", img)
        print(fname)
        cv2.imshow('show', img_resize)
        i = + 1
        cv2.waitKey(100)
N_OK = len(objpoints)
K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
rms, _, _, _, _ = \
    cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 1e-6)
    )

print("Found " + str(N_OK) + " valid images for calibration")
print("DIM=" + str(_img_shape[::-1]))
print("K=np.array(" + str(K.tolist()) + ")")
print("D=np.array(" + str(D.tolist()) + ")")


def save_data():
    fs = cv2.FileStorage("entaniya_13_new_11192022.yaml", cv2.FILE_STORAGE_WRITE)
    fs.write("camera_matrix", K)
    fs.write("dist_coeffs", D)
    fs.write("resolution", np.int32(gray.shape[::-1]))
    # fs.write("project_matrix", project_matrix)
    # fs.write("scale_xy", np.float32(scale_xy))
    # fs.write("shift_xy", np.float32(shift_xy))
    fs.release()


# save_data()