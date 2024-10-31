from PIL import Image, ImageStat
import zipfile
import os

# Caminho da imagem
image_path = 'images3.jpg'

# Função para dividir a imagem em n partes (n x n)
def split_image_into_frames(img, n):
    # Converter imagem para RGB se estiver em modo de paleta
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

# Função para verificar as posições vazias ou ocupadas
def verificar_ocupacao(frames, tolerancia=0.05, margem=200):
    posicoes_ocupadas = []
    for i, frame in enumerate(frames):
        stat = ImageStat.Stat(frame)
        media = stat.mean
        variancia = stat.var

        # Critério para verificar ocupação com base em média e variância
        if any(v < margem for v in media) or any(v > tolerancia for v in variancia):
            posicoes_ocupadas.append(i)
    return posicoes_ocupadas

# Configuração para dividir a imagem em n x n partes
n = 4  # Exemplo: para uma divisão de 4x4, altere esse valor conforme necessário
img = Image.open(image_path)

# Dividir a imagem e verificar ocupação
frames = split_image_into_frames(img, n)
posicoes_ocupadas = verificar_ocupacao(frames)
print("Posições ocupadas:", posicoes_ocupadas)

# Função para salvar os frames divididos
def save_frames(frames, output_folder='frames'):
    os.makedirs(output_folder, exist_ok=True)
    for idx, frame in enumerate(frames):
        frame.save(os.path.join(output_folder, f'frame_{idx}.png'))
    print(f"{len(frames)} frames salvos com sucesso em '{output_folder}'!")

save_frames(frames)

# Compactar os frames em um ZIP
def compress_frames(output_folder='frames', zip_name='frames.zip'):
    with zipfile.ZipFile(zip_name, 'w') as zf:
        for file in os.listdir(output_folder):
            zf.write(os.path.join(output_folder, file), arcname=file)
    print(f"Frames compactados em {zip_name}")

compress_frames()
