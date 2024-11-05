from PIL import Image
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
    for i in range(n):
        for j in range(n):
            left = j * frame_width
            upper = i * frame_height
            right = left + frame_width
            lower = upper + frame_height
            frame = img.crop((left, upper, right, lower))
            frames.append(frame)
    return frames

def verificar_motor(frame):
    frame = frame.resize((128, 128))
    img_array = np.array(frame) / 255.0 
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return prediction[0][0] < 0.5

def process_image(image_path, zip_obj):
    img = Image.open(image_path)
    frames = split_image_into_frames(img, 4)
    posicoes_motor = []

    for idx, frame in enumerate(frames):
        if verificar_motor(frame):
            posicoes_motor.append(idx)
        print(f"Frame {idx}: {'Motor' if idx in posicoes_motor else 'Vazio'}")

    resultado_txt = "\n".join([f"Posição {i}: {'Motor' if i in posicoes_motor else 'Vazio'}" for i in range(len(frames))])
    print("Resultado gerado:", resultado_txt) 

    zip_obj.writestr("resultado.txt", resultado_txt)

    for idx, frame in enumerate(frames):
        with io.BytesIO() as frame_buffer:
            frame.save(frame_buffer, format="PNG")
            frame_buffer.seek(0)
            zip_obj.writestr(f"frame_{idx}.png", frame_buffer.read())
        print(f"Frame {idx} salvo no ZIP")