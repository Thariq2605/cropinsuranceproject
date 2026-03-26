import cv2
import numpy as np
from PIL import Image
import os


def load_gray(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"⚠️ Warning: Image not found at {image_path}")
            return None
        img = Image.open(image_path).convert("L")
        return np.array(img)
    except Exception as e:
        print(f"❌ Error loading image {image_path}: {e}")
        return None


def orb_match(img1_path, img2_path, ratio_threshold=0.20):
    img1 = load_gray(img1_path)
    img2 = load_gray(img2_path)

    if img1 is None or img2 is None:
        return False, 0, 0

    # Increase features for better accuracy
    orb = cv2.ORB_create(nfeatures=5000)

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return False, 0, 0

    # Brute Force Matcher with Hamming distance for ORB
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    
    try:
        matches = bf.knnMatch(des1, des2, k=2)
    except Exception as e:
        print(f"Match error: {e}")
        return False, 0, 0

    # Lowe's ratio test
    good_matches = []
    for m_n in matches:
        if len(m_n) == 2:
            m, n = m_n
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

    total_keypoints = min(len(kp1), len(kp2))
    if total_keypoints == 0:
        return False, 0, 0
        
    match_ratio = len(good_matches) / total_keypoints

    # Stricter threshold for duplicates
    is_duplicate = match_ratio >= ratio_threshold

    return is_duplicate, len(good_matches), match_ratio
