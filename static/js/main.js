let selectedFiles = [];
let processedFiles = [];

const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const toleranciaSlider = document.getElementById('tolerancia');
const toleranciaValue = document.getElementById('toleranciaValue');
const processBtn = document.getElementById('processBtn');
const downloadAllBtn = document.getElementById('downloadAllBtn');
const progressBar = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const results = document.getElementById('results');

toleranciaSlider.addEventListener('input', (e) => {
    toleranciaValue.textContent = e.target.value;
});

fileInput.addEventListener('change', async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (data.files) {
            selectedFiles = data.files;
            displayFileList();
            showPreview();
        }
    } catch (error) {
        console.error('Erro ao fazer upload:', error);
        alert('Erro ao fazer upload dos arquivos');
    }
});

function displayFileList() {
    fileList.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.textContent = file.filename;
        fileList.appendChild(div);
    });
}

function showPreview() {
    results.innerHTML = '<h3 style="font-size: 11px; margin-bottom: 10px;">Preview das Imagens Selecionadas:</h3>';
    
    selectedFiles.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = `
            <h3>${file.filename}</h3>
            <div class="image-preview">
                <div class="preview-box">
                    <img src="/uploads/${file.filename}" alt="Original" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22%3E%3C/svg%3E'">
                    <div class="preview-label">Original</div>
                </div>
                <div class="preview-box">
                    <div style="padding: 20px; color: #808080; font-size: 10px;">Aguardando processamento...</div>
                    <div class="preview-label">Processada</div>
                </div>
            </div>
        `;
        results.appendChild(div);
    });
}

processBtn.addEventListener('click', async () => {
    if (selectedFiles.length === 0) {
        alert('Selecione pelo menos uma imagem');
        return;
    }
    
    processBtn.disabled = true;
    progressBar.style.width = '0%';
    progressText.textContent = '0%';
    
    const tolerancia = parseInt(toleranciaSlider.value);
    
    try {
        const response = await fetch('/processar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                files: selectedFiles,
                tolerancia: tolerancia
            })
        });
        
        const data = await response.json();
        processedFiles = [];
        
        if (data.resultados) {
            let processed = 0;
            data.resultados.forEach((resultado, index) => {
                if (resultado.success) {
                    processedFiles.push(resultado.processed);
                    updateResultPreview(resultado, index);
                    processed++;
                } else {
                    showError(resultado, index);
                }
                
                const progress = ((index + 1) / data.resultados.length) * 100;
                progressBar.style.width = progress + '%';
                progressText.textContent = Math.round(progress) + '%';
            });
            
            if (processedFiles.length > 0) {
                downloadAllBtn.disabled = false;
            }
        }
    } catch (error) {
        console.error('Erro ao processar:', error);
        alert('Erro ao processar as imagens');
    } finally {
        processBtn.disabled = false;
        progressBar.style.width = '100%';
        progressText.textContent = '100%';
    }
});

function updateResultPreview(resultado, index) {
    const resultItems = results.querySelectorAll('.result-item');
    if (resultItems[index]) {
        const previewBoxes = resultItems[index].querySelectorAll('.preview-box');
        if (previewBoxes[1]) {
            previewBoxes[1].innerHTML = `
                <img src="${resultado.url_processada}" alt="Processada" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22%3E%3C/svg%3E'">
                <div class="preview-label">Processada</div>
                <button class="download-btn" onclick="downloadFile('${resultado.processed}')">Baixar</button>
            `;
        }
        
        const successMsg = document.createElement('div');
        successMsg.className = 'success-message';
        successMsg.textContent = '✓ Processada com sucesso!';
        resultItems[index].appendChild(successMsg);
    }
}

function showError(resultado, index) {
    const resultItems = results.querySelectorAll('.result-item');
    if (resultItems[index]) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-message';
        errorMsg.textContent = '✗ Erro: ' + (resultado.error || 'Erro desconhecido');
        resultItems[index].appendChild(errorMsg);
    }
}

function downloadFile(filename) {
    window.location.href = `/download/${filename}`;
}

downloadAllBtn.addEventListener('click', async () => {
    if (processedFiles.length === 0) {
        alert('Nenhuma imagem processada para baixar');
        return;
    }
    
    try {
        const response = await fetch('/download_all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                files: processedFiles
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'imagens_sem_fundo.zip';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Erro ao baixar arquivos');
        }
    } catch (error) {
        console.error('Erro ao baixar:', error);
        alert('Erro ao baixar os arquivos');
    }
});

window.downloadFile = downloadFile;

