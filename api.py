from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.Agente import AI_agente_extrator
from utils.pdf_to_img_to_text import extrair_texto_de_pdf_scaneado
import uvicorn
import json

app = FastAPI(title="API de Extrator Multimodal com IA")

# Inicializar o agente
try:
    agent = AI_agente_extrator()
except Exception as e:
    print(f"Erro ao inicializar o agente: {e}")
    agent = None

@app.get("/")
async def root():
    return {"message": "API de Extrator Multimodal com IA está rodando"}

@app.post("/extract/ocr")
async def extract_ocr(file: UploadFile = File(...)):
    """
    Extrai dados de um PDF escaneado usando OCR e depois o agente de IA.
    """
    if not agent:
        raise HTTPException(status_code=500, detail="Agente não inicializado")
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF")

    try:
        # Ler conteúdo do arquivo
        content = await file.read()
        
        # Extrair texto usando OCR
        text = extrair_texto_de_pdf_scaneado(content)
        
        if not text:
             raise HTTPException(status_code=500, detail="Falha ao extrair texto via OCR")

        # Analisar texto com o agente
        result_json = await agent.extrair_dados_txt(text)
        
        return json.loads(result_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/direct")
async def extract_direct(file: UploadFile = File(...)):
    """
    Extrai dados de um PDF enviando o conteúdo binário diretamente para o agente de IA.
    """
    if not agent:
        raise HTTPException(status_code=500, detail="Agente não inicializado")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF")

    try:
        # Ler conteúdo do arquivo
        content = await file.read()
        
        # Analisar PDF diretamente com o agente
        result_json = await agent.extrair_dados_pdf(content)
        
        return json.loads(result_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
