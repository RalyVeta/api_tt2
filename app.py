from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Cargar el modelo y las clases
model = load_model('modelo.h5')
class_names = ["clase_0", "clase_1", "clase_2", "clase_3", "clase_4", "clase_5", "clase_6", "clase_7", "clase_8", "clase_9", "clase_10", "clase_11", "clase_12"]

# Función para cargar y preprocesar la imagen
def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(180, 180))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Función para predecir la clase de la imagen
def predict_image_class(img_path):
    img_array = load_and_preprocess_image(img_path)
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    
    if predicted_class_index < len(class_names):
        predicted_class_name = class_names[predicted_class_index]
        return predicted_class_name, predictions, int(predicted_class_index)
    else:
        return "Clase no encontrada", predictions, None

# Ruta para predecir la clase de una imagen
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No se encontró ninguna imagen en la solicitud', 400

    file = request.files['file']
    if file.filename == '':
        return 'No se proporcionó un nombre de archivo válido', 400

    img_path = 'temp.jpg'  # Guardar la imagen temporalmente
    file.save(img_path)

    predicted_class_name, predictions, predicted_class_index = predict_image_class(img_path)

    # Eliminar la imagen temporal
    os.remove(img_path)

    response = {
        'predicted_class': predicted_class_name if predicted_class_index is not None else None,
        'predicted_class_index': predicted_class_index,
        'predictions': predictions.tolist()
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)