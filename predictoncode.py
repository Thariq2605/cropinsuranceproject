import cv2
import numpy as np
import tensorflow as tf

# Load trained MobileNet model
model = tf.keras.models.load_model("crop_mobilenet_model.h5")

# MUST match training output
class_names = ['cotton', 'maize', 'rice', 'wheat']

IMG_SIZE = 224

def predict_crop(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    crop_index = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    return class_names[crop_index], confidence
