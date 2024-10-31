from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import cv2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
# model_path = "./bestModel.h5"  # Ensure this path is correct
model = tf.keras.models.load_model("C:/Users/Pavilion/OneDrive/Desktop/Tumor Detection Web App/backend/models/bestModel.h5")

# Function to preprocess images
def preprocess_image(image):
    """
    Preprocess the input image in the same way as the training data.
    Args:
        image (PIL.Image): Input image.
    Returns:
        np.ndarray: Preprocessed image array.
    """
    # Convert PIL image to OpenCV format
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Resize the image
    img = cv2.resize(image, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        # Find the extreme points and crop the image
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        new_img = img[extTop[1]:extBot[1], extLeft[0]:extRight[0]].copy()
        new_img = cv2.resize(new_img, (224, 224), interpolation=cv2.INTER_CUBIC)
    else:
        new_img = img  # Use the resized image if no contours found

    # Normalize pixel values
    img_array = new_img / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Preprocess the image
        image = Image.open(file)
        image = ImageOps.exif_transpose(image)  # Correct orientation if needed
        image = preprocess_image(image)

        # Make prediction
        prediction = model.predict(image)[0][0]
        predicted_class = "Healthy" if prediction < 0.5 else "Tumor"

        return jsonify({'prediction': predicted_class, 'confidence': float(prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
