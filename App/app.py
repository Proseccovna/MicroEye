# Ваш app.py

from flask import Flask, render_template, request, send_from_directory, url_for
import os
import subprocess
from PIL import Image
import random
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

def detect(file_path):
    model_path = 'weights.pt'
    command = f"python yolov5/detect.py --weights {model_path} --img-size 640 --source {file_path}"
    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return result.stdout

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def process_image(file_path, result):
    image = Image.open(file_path)

    # Здесь добавьте логику обработки изображения с учетом результатов предсказания
    # Например, добавьте аннотации или выделите клетки на изображении

    # Генерируем уникальное имя для обработанного изображения
    timestamp = datetime.timestamp(datetime.now())
    processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'processed_{timestamp}.png')
    image.save(processed_image_path)

    return processed_image_path

@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file and allowed_file(file.filename):
        # Сохраняем загруженный файл
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Здесь добавьте логику для подсчета клеток на фотографии с использованием вашей модели YOLO
        detection_result = detect(file_path)

        # Здесь добавьте логику обработки изображения после предсказания
        processed_image_path = process_image(file_path, detection_result)

        return render_template('index.html', result=detection_result, images=os.listdir(app.config['UPLOAD_FOLDER']), original_image=file.filename, processed_image=os.path.basename(processed_image_path))

    return render_template('index.html', error='Invalid file type')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

