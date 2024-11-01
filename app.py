from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from processamento import process_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "Nenhum arquivo encontrado.", 400
    
    file = request.files['image']
    if file.filename == '':
        return "Nenhum arquivo selecionado.", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Processa a imagem e gera o ZIP
    zip_path = os.path.join(app.config['PROCESSED_FOLDER'], 'frames_e_resultado.zip')
    process_image(file_path, zip_path)

    # Retorna o ZIP como resposta
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
