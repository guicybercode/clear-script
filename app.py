from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import zipfile
import tempfile
from remover_fundo import processar_imagem, PASTA_SEM_FUNDO, PASTA_ORIGINAIS, criar_pastas

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    files = request.files.getlist('files')
    uploaded_files = []
    
    criar_pastas()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append({
                'filename': filename,
                'path': filepath
            })
    
    return jsonify({'files': uploaded_files})

@app.route('/processar', methods=['POST'])
def processar():
    data = request.json
    files = data.get('files', [])
    tolerancia = int(data.get('tolerancia', 10))
    
    resultados = []
    
    for file_info in files:
        try:
            filepath = file_info.get('path')
            if not os.path.exists(filepath):
                resultados.append({
                    'filename': file_info.get('filename'),
                    'success': False,
                    'error': 'Arquivo não encontrado'
                })
                continue
            
            imagem_saida = processar_imagem(filepath, tolerancia, salvar_original=True)
            nome_arquivo = os.path.basename(imagem_saida)
            
            resultados.append({
                'filename': file_info.get('filename'),
                'processed': nome_arquivo,
                'success': True,
                'url_original': f'/uploads/{file_info.get("filename")}',
                'url_processada': f'/sem_fundo/{nome_arquivo}'
            })
        except Exception as e:
            resultados.append({
                'filename': file_info.get('filename'),
                'success': False,
                'error': str(e)
            })
    
    return jsonify({'resultados': resultados})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/sem_fundo/<filename>')
def sem_fundo_file(filename):
    return send_from_directory(PASTA_SEM_FUNDO, filename)

@app.route('/originais/<filename>')
def original_file(filename):
    return send_from_directory(PASTA_ORIGINAIS, filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PASTA_SEM_FUNDO, filename, as_attachment=True)

@app.route('/download_all', methods=['POST'])
def download_all():
    data = request.json
    filenames = data.get('files', [])
    
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    
    with zipfile.ZipFile(temp_zip.name, 'w') as zipf:
        for filename in filenames:
            filepath = os.path.join(PASTA_SEM_FUNDO, filename)
            if os.path.exists(filepath):
                zipf.write(filepath, filename)
    
    return send_file(temp_zip.name, mimetype='application/zip', as_attachment=True, download_name='imagens_sem_fundo.zip')

if __name__ == '__main__':
    criar_pastas()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)

