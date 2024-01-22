from ultralytics import YOLO
import torch
import PIL
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import subprocess


def detect(file_path):
    # Формируем команду для выполнения
    model_path = '/home/tata/DS_bootcamp/Final project/App/model/weights.pt'
    command = f"python detect.py --weights {model_path} --img-size 640 --source {image_path}"

    # Вызываем команду
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Возвращаем результат выполнения команды
    return result.stdout



