from PIL import Image, ImageStat
import zipfile
import os

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

def verificar_ocupacao(frames, diferenca_tolerada=30, variancia_tolerada=1000):
    posicoes_ocupadas = []
    referencia_vazia = ImageStat.Stat(frames[2]).mean
    variancia_vazia = sum(ImageStat.Stat(frames[2]).var) / 3

    for i, frame in enumerate(frames):
        stat = ImageStat.Stat(frame)
        media = stat.mean
        variancia = sum(stat.var) / 3
        diferenca = sum(abs(media[j] - referencia_vazia[j]) for j in range(3)) / 3

        if diferenca > diferenca_tolerada or variancia > variancia_vazia + variancia_tolerada:
            posicoes_ocupadas.append(i)
    return posicoes_ocupadas

def exportar_resultado(posicoes_ocupadas, total_frames, output_file):
    with open(output_file, 'w') as f:
        for i in range(total_frames):
            status = "Ocupado" if i in posicoes_ocupadas else "Vazio"
            f.write(f"Posição {i}: {status}\n")

def process_image(image_path, zip_path):
    img = Image.open(image_path)
    frames = split_image_into_frames(img, 4)
    posicoes_ocupadas = verificar_ocupacao(frames)

    output_folder = os.path.dirname(zip_path)
    os.makedirs(output_folder, exist_ok=True)

    txt_path = os.path.join(output_folder, "resultado.txt")
    exportar_resultado(posicoes_ocupadas, len(frames), txt_path)

    with zipfile.ZipFile(zip_path, 'w') as zf:
        for idx, frame in enumerate(frames):
            frame_path = os.path.join(output_folder, f'frame_{idx}.png')
            frame.save(frame_path)
            zf.write(frame_path, arcname=f'frame_{idx}.png')
        zf.write(txt_path, arcname="resultado.txt")
