from PIL import Image
import sys
import os
import shutil

PASTA_ORIGINAIS = "originais"
PASTA_SEM_FUNDO = "sem_fundo"

def criar_pastas():
    os.makedirs(PASTA_ORIGINAIS, exist_ok=True)
    os.makedirs(PASTA_SEM_FUNDO, exist_ok=True)

def remover_fundo_branco(imagem_entrada, imagem_saida=None, tolerancia=10):
    img = Image.open(imagem_entrada)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    dados = img.getdata()
    novos_dados = []
    
    for item in dados:
        if item[0] > 255 - tolerancia and item[1] > 255 - tolerancia and item[2] > 255 - tolerancia:
            novos_dados.append((255, 255, 255, 0))
        else:
            novos_dados.append(item)
    
    img.putdata(novos_dados)
    
    if imagem_saida is None:
        nome_arquivo = os.path.basename(imagem_entrada)
        nome_base = os.path.splitext(nome_arquivo)[0]
        imagem_saida = os.path.join(PASTA_SEM_FUNDO, f"{nome_base}.png")
    
    criar_pastas()
    img.save(imagem_saida, 'PNG')
    return imagem_saida

def processar_imagem(imagem_entrada, tolerancia=10, salvar_original=True):
    criar_pastas()
    
    if not os.path.exists(imagem_entrada):
        raise FileNotFoundError(f"Arquivo '{imagem_entrada}' não encontrado!")
    
    if salvar_original:
        nome_arquivo = os.path.basename(imagem_entrada)
        destino_original = os.path.join(PASTA_ORIGINAIS, nome_arquivo)
        
        if not os.path.exists(destino_original):
            shutil.copy2(imagem_entrada, destino_original)
    
    imagem_saida = remover_fundo_branco(imagem_entrada, None, tolerancia)
    return imagem_saida

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python remover_fundo.py <imagem_entrada> [tolerancia]")
        print("\nExemplo:")
        print("  python remover_fundo.py alura.png")
        print("  python remover_fundo.py alura.png 20")
        sys.exit(1)
    
    imagem_entrada = sys.argv[1]
    tolerancia = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    try:
        processar_imagem(imagem_entrada, tolerancia)
        print(f"Imagem processada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

