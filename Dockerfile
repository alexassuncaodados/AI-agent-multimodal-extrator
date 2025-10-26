# Usando imagem base do Python

FROM python:3.13.8-slim
 
# Diretório de trabalho dentro do container

WORKDIR /app
 
# Copia apenas o requirements.txt primeiro

COPY requirements.txt /app/
 
# Instala as dependências

RUN pip install --no-cache-dir -r requirements.txt
 
# Copia o restante da aplicação

COPY . /app/