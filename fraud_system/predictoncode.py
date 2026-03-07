import cv2
import numpy as np
import tensorflow as tf
import os

print("PREDICTION FILE LOADED")

# Get correct path of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR,"crop_mobilenet_model.keras")

print("MODEL PATH:",MODEL_PATH)
print("FILE EXISTS:",os.path.exists(MODEL_PATH))

model = None

def load_model_once():
    global model
    if model is None:
        print("Loading model...")
        model = tf.keras.models.load_model(MODEL_PATH,compile=False)
        print("model loaded sucessfully")

class_names = ['cotton', 'maize', 'rice', 'wheat']
IMG_SIZE = 224

def predict_crop(image_path):
    load_model_once()

    img = cv2.imread(image_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    crop_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100

    return class_names[crop_index], confidence