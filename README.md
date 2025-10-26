# AI Agent Multimodal Extrator

Agente de IA para extração de dados de arquivos PDF. Utiliza duas abordagens: OCR para PDFs scaneados e envio direto de PDF ao agente de IA.

## Tecnologias Utilizadas

- PydanticAI
- Pydantic
- Tesseract OCR
- Poppler


## Funcionalidades

- Como exemplo é feito a extração de dados de Notas Fiscais de Serviço (NFSe)
- Duas abordagens de processamento:
  - **OCR**: Conversão de PDF para imagem e extração de texto via Tesseract
  - **Input de Documento**: Envio do arquivo PDF diretamente ao agente de IA
- Estruturação de dados extraídos em formato JSON

#### 💻 Notebook com exemplos
[Exemplos de uso do agente de IA usando OCR e input de PDF](https://github.com/alexassuncaodados/AI-agent-multimodal-extrator/blob/main/app.ipynb)

## Estrutura do Projeto

```
.
├── app.py                      # Script de execução simples
├── app.ipynb                   # Notebook com exemplos
├── utils/
│   ├── Agente.py              # Configuração e lógica do agente de IA usando pydantic-ai e orientação a objetos
│   ├── BaseModel.py           # Modelos Pydantic para validação
│   └── pdf_to_img_to_text.py  # Funções de OCR
├── nota_fiscal/               # Diretório para arquivos PDF
├── requirements.txt           # Dependências do projeto
├── Dockerfile                 # Configuração Docker
└── docker-compose.yml         # Orquestração Docker
```

## Requisitos

- Python 3.13+
- Tesseract OCR (NÃO incluso no projeto, disponível para download em https://github.com/UB-Mannheim/tesseract/wiki)
- Poppler (NÃO incluso no projeto, disponível para download em https://github.com/oschwartz10612/poppler-windows/releases)
- API Key do Google Gemini

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
3. Instale as dependências:
4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env e adicione sua API Key do Google
```

## Uso

### Execução Local

```bash
python app.py
```

O script processa todos os PDFs na pasta `nota_fiscal/` e exibe os dados extraídos.

### Execução com Docker

```bash
docker-compose up
```

## Dados Extraídos do exemplo

O agente extrai os seguintes campos de cada nota fiscal:

- `descricao_servico`: Descrição dos serviços prestados
- `valor_servico`: Valor do serviço
- `numero_nf`: Número da nota fiscal
- `data_emissao`: Data de emissão (formato YYYY-MM-DD)
- `valor_total`: Valor total da nota
- `cnpj`: CNPJ do prestador (apenas números)

#### 💻 Notebook com exemplos
[Exemplos de uso do agente de IA usando OCR e input de PDF](https://github.com/alexassuncaodados/AI-agent-multimodal-extrator/blob/main/app.ipynb)

## Roadmap

- [x] **Extrator de Dados**: Agente de IA para extração de dados de notas fiscais
- [ ] **Validação de Documento**: Verifica se o documento é uma nota fiscal
- [ ] **API REST** (FastAPI): Endpoints para processamento de PDFs
- [ ] **Dashboard**: Interface web para envio e análise de arquivos
- [x] **Dockerização**: Imagem Docker para fácil implantação


## Configuração de Variáveis de Ambiente

Veja `.env.example` para referência:

```
api_key=sua-chave-api-google
TESSERACT_PATH=/caminho/para/tesseract
```


## Autor Alex Silva de Assunção
- [LinkedIn](https://www.linkedin.com/in/alexassuncaodata/)- [GitHub](https://github.com/alexassuncaodados)
## Contato
- Email: [alexassuncao.dados@email.com](mailto:alexassuncao.dados@email.com)

