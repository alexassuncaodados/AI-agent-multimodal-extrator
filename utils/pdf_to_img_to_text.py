from pdf2image import convert_from_bytes
import pytesseract
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o diretório raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

# Configuração do Poppler
poppler_path = os.path.join(PROJECT_ROOT, "poppler-25.07.0", "Library", "bin")



from typing import Union

def extrair_texto_de_pdf_scaneado(caminho_pdf: Union[str, bytes], idioma='por')-> str:
    """
    Extrai texto de um PDF scaneado usando OCR (Tesseract).

    Argumentos:
        caminho_pdf (str): O caminho para o arquivo PDF.
        idioma (str): O código do idioma para o Tesseract (ex: 'por' para português).
    
    Retorna:
        str: O texto completo extraído de todas as páginas.
    """
    
    # 1. Converter PDF para uma lista de imagens (objetos PIL)
    try:
        if isinstance(caminho_pdf, bytes):
            pdf_bytes = caminho_pdf
        else:
            pdf_bytes = open(caminho_pdf, 'rb').read()
            
        imagens = convert_from_bytes(pdf_bytes, poppler_path=poppler_path, dpi=300)
    except Exception as e:
        print(f"Erro ao converter PDF. Verifique se o Poppler está instalado e no PATH.")
        print(f"Erro: {e}")
        return None

    texto_completo = ""
    
    print(f"PDF tem {len(imagens)} página(s). Processando...")

    # 2. Iterar por cada imagem/página e aplicar OCR
    for i, imagem in enumerate(imagens):
        print(f"Processando página {i+1}...")
        
        # 3. Usar pytesseract para extrair o texto da imagem
        try:
            texto = pytesseract.image_to_string(imagem, lang=idioma)
            texto_completo += f"--- PÁGINA {i+1} ---\n"
            texto_completo += texto + "\n\n"
        except pytesseract.TesseractNotFoundError:
            print("ERRO: O executável do Tesseract não foi encontrado.")
            print("Verifique se ele está instalado e no PATH do seu sistema.")
            return None
        except Exception as e:
            print(f"Erro no Tesseract na página {i+1}: {e}")

    print("Processamento concluído.")
    # 4. Retornar o texto completo exraído das páginas do PDF
    return texto_completo





