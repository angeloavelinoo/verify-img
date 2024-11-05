from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from processamento import process_image
import io
import zipfile

app = Flask(__name__)
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

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        process_image(file_path, zf)  

    with open("frames_e_resultado_debug.zip", "wb") as f:
        f.write(zip_buffer.getvalue())

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='frames_e_resultado.zip')

if __name__ == '__main__':
    app.run(debug=True)
