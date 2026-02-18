def crop_damage_analysis(image_path):
    import cv2
    import numpy as np

    # Read and resize image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))

    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define damaged crop color range (dry / yellow / brown)
    lower_damage = np.array([10, 40, 40])
    upper_damage = np.array([30, 255, 200])

    # Create mask
    damage_mask = cv2.inRange(hsv, lower_damage, upper_damage)

    # Pixel calculation
    damaged_pixels = cv2.countNonZero(damage_mask)
    total_pixels = img.shape[0] * img.shape[1]

    damage_percentage = (damaged_pixels / total_pixels) * 100

    return float(round(damage_percentage, 2))

if __name__ == "__main__":
    image_path = r"C:\Users\moham\Downloads\OIP (2).jpeg"
    damage = crop_damage_analysis(image_path)

    print("Crop Damage Percentage:", damage, "%")
