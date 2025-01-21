# Usar imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt requirements.txt

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte para dentro do container
COPY ./src /app/src

# Copiar a pasta de dados para o container (opcional, se os dados forem necessários localmente)
COPY ./data /app/data

# Definir o comando padrão o script
CMD ["python", "src/ingestion.py", "src/configs/icf.json"]