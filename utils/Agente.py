import os
from typing import Optional
from dotenv import load_dotenv

#importa pydantic-ai Agent
from pydantic_ai import Agent

#importa pydantic-ai BinaryContent para tratamento de arquivos binários
from pydantic_ai import BinaryContent

# Importa o modelo e o provedor do Google Gemini no pydantic-ai
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

# Importa os modelos de dados de saída
from utils.BaseModel import ExtracaoOutput



class AgenteConfig:
    """Gerencia configurações do agente."""
    # Modelo padrão do Google Gemini
    DEFAULT_MODEL = 'gemini-2.5-flash'
    # DEFAULT_MODEL = 'gemini-2.0-flash-lite'

    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_model: str = DEFAULT_MODEL,
        auto_load_env: bool = True
    ):
        if auto_load_env:
            load_dotenv()

        self.api_key = api_key or os.getenv("api_key")
        self.llm_model = llm_model

        if not self.api_key:
            raise ValueError("API Key não encontrada ou variável de ambiente não definida.")


class PromptManager:
    """Gerencia prompts do sistema."""


    EXTRACAO_PROMPT = """
        Você é um agente de IA especialista em processamento de documentos fiscais brasileiros. Sua principal tarefa é analisar o conteúdo de uma Nota Fiscal de Serviço em formato de documento (PDF) ou texto extraído de um docuemnto (PDF), extrair informações cruciais e retorná-las em um formato estruturado, de acordo com o modelo Pydantic fornecido.

        **Instruções Gerais:**

        1.  **Entrada:** Você receberá um documento, que é uma representação de uma Nota Fiscal de Serviço. Utilize o recurso de `Document Input` para ler e interpretar diretamente o conteúdo textual do documento.
        2.  **Objetivo:** Seu objetivo é preencher de forma precisa e completa o modelo Pydantic `ExtracaoOutput` com os dados extraídos do documento.
        3.  **Contexto:** A Nota Fiscal de Serviço é um documento oficial que registra a prestação de serviços. Preste muita atenção aos seguintes campos:
            * **Descrição do Serviço:** O detalhamento do serviço que foi executado.
            * **Valor do Serviço:** O valor a ser pago pelo serviço prestado.
            * **Número da Nota:** O número da nota fiscal.
            * **Data de emissão:** A data em que a nota fiscal foi emitida.
            * **Valor Total:** O valor total da nota fiscal (bruto).
            * **CNPJ do Prestador:** CNPJ de quem emitiu a nota.

        **Regras de Extração:**

        * **Precisão é fundamental:** Extraia os valores exatamente como aparecem no documento. Não invente ou infira informações que não estão presentes.
        * **Formatos:**
            * Para valores monetários, extraia o número e formate-o como um `float` (ex: "R$ 1.500,50" deve ser extraído como `1500.50`).
            * Para CNPJ e CPF, extraia apenas os números.
            * Para datas, siga o formato `YYYY-MM-DD`. Se a data no documento estiver em outro formato (ex: DD/MM/YYYY), faça a conversão.
        * **Ambiguidade:** Se um campo não for encontrado ou se a informação for ambígua, retorne `None` para aquele campo específico. Não tente adivinhar.
        * **Foco no Conteúdo:** Analise todo o texto extraído do documento para localizar as informações. Ignore elementos de layout, como logos ou tabelas, e foque nos rótulos e nos dados textuais.

        **Exemplo de Saída:**
        ```
        {
            "descricao_servico": "Consultoria em TI",
            "valor_servico": 1500.00,
            "numero_nf": 123456,
            "data_emissao": "2023-10-01",
            "valor_total": 1500.00,
            "cnpj": "12345678000195"
        }
        """


class AI_agente_extrator:
    """Agente de IA para extração de notas fiscais."""

    def __init__(self, config: Optional[AgenteConfig] = None):
        self.config = config or AgenteConfig()
        self._agent = self._inicializar_agente()

    def _inicializar_agente(self) -> Agent:
        """Inicializa e retorna o agente de IA."""
        try:
            model = GoogleModel(
                self.config.llm_model,
                provider=GoogleProvider(api_key=self.config.api_key)
            )
            print(f'Modelo {self.config.llm_model} criado com sucesso.')

            return Agent(
                model=model,
                system_prompt=PromptManager.EXTRACAO_PROMPT,
                output_type=ExtracaoOutput
            )
        except Exception as e:
            raise Exception(f"Erro ao inicializar agente: {str(e)}") from e

    @property
    def agent(self) -> Agent:
        """Retorna o agente de IA configurado."""
        return self._agent

    async def extrair_dados_txt(self, conteudo: str) -> ExtracaoOutput:
        """Extrai dados a partir de texto extraído da nota fiscal."""
        resultado = await self.agent.run(conteudo)
        return resultado.output.model_dump_json()
    
    async def extrair_dados_pdf(self, conteudo: str) -> ExtracaoOutput:
        """Extrai dados de um arquivo PDF da nota fiscal."""
        resultado = await self.agent.run(
            [BinaryContent(conteudo, media_type='application/pdf')]
        )
        return resultado.output.model_dump_json()