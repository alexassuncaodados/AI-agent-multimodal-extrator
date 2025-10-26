# Importações necessárias
import asyncio
from utils.agente_oo import AgenteCharla
# from utils.AgenteCharla import criar_agente_charla
from utils.pdf_to_img_to_text import extrair_texto_de_pdf_scaneado

from pathlib import Path



def main_sync():
    # Inicialização do agente de IA
    try:
        agent = AgenteCharla()
        print("Agente criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar agente: {e}")
        return  
    
    # Verificação da pasta de notas fiscais
    pasta_notas = Path('nota_fiscal')
    if not pasta_notas.exists():
        print(f"Pasta '{pasta_notas}' não encontrada.")
        return
    
    # Busca todos os arquivos PDF na pasta
    arquivos_pdf = list(pasta_notas.glob('*.pdf'))
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta 'nota_fiscal'.")
        return
    
    print(f"Encontrados {len(arquivos_pdf)} arquivos PDF para processar...")
    
    # Função assíncrona para processar múltiplos documentos
    async def process_documents():
        resultados = []
        
        for i, arquivo_pdf in enumerate(arquivos_pdf, 1):
            print(f"\n--- Processando arquivo {i}/{len(arquivos_pdf)}: {arquivo_pdf.name} ---")
            
            try:
                # # Faz a extração de dados do PDF
                # arquivobyte = arquivo_pdf.read_bytes()
                # resultado = await agent.run(
                #     [BinaryContent(arquivobyte, media_type='application/pdf')]
                # )
                arquivo = extrair_texto_de_pdf_scaneado(arquivo_pdf)
                # print(arquivo)
                resultado = await agent.extrair_dados(arquivo)
                
                # Exibe o resultado no console
                print("Resultado extraído:")
                print(resultado.model_dump())
                
                # Adiciona à lista de resultados
                resultados.append({
                    'arquivo': arquivo_pdf.name,
                    'dados': resultado.model_dump()
                })
                
            except Exception as e:
                print(f"Erro ao processar {arquivo_pdf.name}: {e}")
                resultados.append({
                    'arquivo': arquivo_pdf.name,
                    'erro': str(e)
                })
        
        return resultados
    
    # Executa a função assíncrona
    return asyncio.run(process_documents())


if __name__ == "__main__":
    main_sync()