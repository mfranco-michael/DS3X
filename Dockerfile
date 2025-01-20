# Usar imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar as dependências para o container
COPY requirements.txt requirements.txt

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte para dentro do container
COPY ./src /app/src

# Definir o comando para rodar o script Python
CMD ["python", "src/main.py"]
