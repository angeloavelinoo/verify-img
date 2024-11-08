from flask import Flask, render_template, request, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from processamento import process_image
import io
import zipfile

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    processed_image = process_image(file_path)
    return send_file(processed_image, mimetype='image/png', as_attachment=True, download_name='imagem_processada.png')


if __name__ == '__main__':
    app.run(debug=True)
