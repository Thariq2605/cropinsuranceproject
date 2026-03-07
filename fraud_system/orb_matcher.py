import cv2
import numpy as np
from PIL import Image


def load_gray(image_path):
    img = Image.open(image_path).convert("L")
    return np.array(img)


def orb_match(img1_path, img2_path, ratio_threshold=0.20):
    img1 = load_gray(img1_path)
    img2 = load_gray(img2_path)

    orb = cv2.ORB_create(nfeatures=3000)

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return False, 0, 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    total_keypoints = min(len(kp1), len(kp2))
    match_ratio = len(good_matches) / total_keypoints

    is_duplicate = match_ratio >= ratio_threshold

    return is_duplicate, len(good_matches), match_ratio
