import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import json

config_path = sys.argv[1]

def run_ingestion(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        p_url = config["p_url"]
        print("usando o arquivo de parametro")
    return p_url    

p_url = run_ingestion(config_path)

def find_link_file(p_url):
    # Realizando a requisição da página
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(p_url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parse do conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Expressão regular para encontrar o padrão href="*.xlsx"
        pattern = r'href="([^"]+\.xlsx)"'

        # Converter o conteúdo do BeautifulSoup para string
        html_as_string = str(soup)

        # Usar re.search para capturar o primeiro link
        match = re.search(pattern, html_as_string)

        if match:
            # Captura o grupo correspondente ao link
            link = match.group(1)
            print(f"Link encontrado: {link}")
            return link
        else:
            print("Nenhum link .xlsx encontrado.")

p_url_download = find_link_file(p_url)

def download_file(p_url_download):
    # Extrair a data do path usando regex
    # Criar o diretório com base na data, se não existir
    # Extrair o nome do arquivo do URL
    file_name = p_url_download.split('/')[-1][0:3]+'.xlsx'

    # Caminho completo para salvar o arquivo
    file_path = os.path.join('./data/raw', file_name)

    # Fazer o download do arquivo
    response = requests.get(p_url_download)

    if response.status_code == 200:
        # Salvar o arquivo no diretório
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Arquivo baixado e salvo como: {file_path}")
    else:
        print(f"Falha ao baixar o arquivo. Status code: {response.status_code}")


download_file(p_url_download)        