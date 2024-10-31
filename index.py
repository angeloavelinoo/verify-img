from PIL import Image
import zipfile
import os

image_path = 'images2.png'

def split_image_into_frames(img, num_frames_x, num_frames_y):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_width, img_height = img.size
    frame_width = img_width // num_frames_x
    frame_height = img_height // num_frames_y

    frames = []
    for i in range(num_frames_y):
        for j in range(num_frames_x):
            left = j * frame_width
            upper = i * frame_height
            right = left + frame_width
            lower = upper + frame_height
            frame = img.crop((left, upper, right, lower))
            frames.append(frame)
    return frames

def verificar_posicoes_vazias(frames, tolerancia=0.90, margem=200):
    posicoes_vazias = []
    for i, frame in enumerate(frames):
        pixels = frame.getdata()
        total_pixels = len(pixels)
        white_pixels = sum(
            1 for pixel in pixels
            if (isinstance(pixel, int) and pixel >= margem) or
               (isinstance(pixel, tuple) and all(channel >= margem for channel in pixel[:3]))
        )
        if white_pixels / total_pixels >= tolerancia:
            posicoes_vazias.append(i)
    return posicoes_vazias

num_frames_x = 3
num_frames_y = 3
img = Image.open(image_path)

frames = split_image_into_frames(img, num_frames_x, num_frames_y)
posicoes_vazias = verificar_posicoes_vazias(frames)
print("Posições vazias:", posicoes_vazias)

def save_frames(frames, output_folder='frames'):
    os.makedirs(output_folder, exist_ok=True)
    for idx, frame in enumerate(frames):
        frame.save(os.path.join(output_folder, f'frame_{idx}.png'))
    print(f"{len(frames)} frames salvos com sucesso em '{output_folder}'!")

save_frames(frames)

def compress_frames(output_folder='frames', zip_name='frames.zip'):
    with zipfile.ZipFile(zip_name, 'w') as zf:
        for file in os.listdir(output_folder):
            zf.write(os.path.join(output_folder, file), arcname=file)
    print(f"Frames compactados em {zip_name}")

compress_frames()
