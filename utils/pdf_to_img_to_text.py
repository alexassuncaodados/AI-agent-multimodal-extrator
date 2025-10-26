from pdf2image import convert_from_bytes
import pytesseract
# Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Poppler (no Windows)
poppler_path = r"C:\Users\Alex\Documents\code\GIT\Case_Charla_Jr_AI_Eng\poppler-25.07.0\Library\bin"



def extrair_texto_de_pdf_scaneado(caminho_pdf, idioma='por'):
    """
    Extrai texto de um PDF scaneado usando OCR (Tesseract).

    Argumentos:
        caminho_pdf (str): O caminho para o arquivo PDF.
        idioma (str): O código do idioma para o Tesseract (ex: 'por' para português).
    
    Retorna:
        str: O texto completo extraído de todas as páginas.
    """
    
    # 1. Converter PDF para uma lista de imagens (objetos PIL)
    # No Windows, você pode precisar especificar o caminho do Poppler:
    # imagens = convert_from_path(caminho_pdf, poppler_path=r'C:\caminho\para\poppler\bin')
    try:
        imagens = convert_from_bytes(open(caminho_pdf, 'rb').read(), poppler_path=poppler_path, dpi=300)
    except Exception as e:
        print(f"Erro ao converter PDF. Verifique se o Poppler está instalado e no PATH.")
        print(f"Erro: {e}")
        return None

    texto_completo = ""
    
    print(f"PDF tem {len(imagens)} página(s). Processando...")

    # 2. Iterar por cada imagem/página e aplicar OCR
    for i, imagem in enumerate(imagens):
        print(f"Processando página {i+1}...")
        
        # Salvar temporariamente a imagem (opcional, mas às vezes ajuda na depuração)
        # nome_arquivo_img = f"pagina_{i}.png"
        # imagem.save(nome_arquivo_img, 'PNG')

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
    return texto_completo





