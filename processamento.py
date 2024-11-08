from PIL import Image, ImageDraw
import numpy as np
from tensorflow.keras.models import load_model
import io

model = load_model("motor_detection_model.keras")

def split_image_into_frames(img, n):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_width, img_height = img.size
    frame_width = img_width // n
    frame_height = img_height // n
    frames = []
    positions = []
    for i in range(n):
        for j in range(n):
            left = j * frame_width
            upper = i * frame_height
            right = left + frame_width
            lower = upper + frame_height
            frame = img.crop((left, upper, right, lower))
            frames.append(frame)
            positions.append((left, upper, right, lower))
    return frames, positions

def verificar_motor(frame):
    frame = frame.resize((128, 128))
    img_array = np.array(frame) / 255.0 
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return prediction[0][0] < 0.5 

def process_image(image_path):
    img = Image.open(image_path)
    frames, positions = split_image_into_frames(img, 4)
    
    draw = ImageDraw.Draw(img)
    posicoes_motor = []

    for idx, frame in enumerate(frames):
        if verificar_motor(frame):
            posicoes_motor.append(idx)
            print(f"Frame {idx}: Motor reconhecido.")
        else:
            print(f"Frame {idx}: Vazio.")
            left, upper, right, lower = positions[idx]
            center_x = (left + right) / 2
            center_y = (upper + lower) / 2
            radius = min((right - left), (lower - upper)) / 2
            draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), outline="red", width=5)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
