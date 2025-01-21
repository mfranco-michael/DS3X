from google.cloud import bigquery
from pandas_gbq import to_gbq
import os
import pandas as pd
from unidecode import unidecode
import time
import sys
import json
from google.cloud import bigquery
config_path = sys.argv[1]

def check_credentials():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    print(f"Caminho das credenciais: {credentials_path}")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credentials_path}")

try:
    check_credentials()
except FileNotFoundError as e:
    print(e)
    raise


def run_ingestion(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        p_file_path  = config["p_file_path"]
        p_sheet_name = config["p_sheet_name"]  
        p_header     = config["p_header"]
        p_tabela_id  = config["p_tabela_id"]
        print("usando o arquivo de parametro")
    return p_file_path, p_sheet_name, p_header,p_tabela_id

def wait_for_file(file_path, timeout=60):
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Arquivo {file_path} não foi encontrado dentro do tempo limite.")
        print(f"Aguardando arquivo: {file_path}")
        time.sleep(5)

def read_xlsx(caminho_arquivo,p_sheet_name,p_header):
    # Ler a aba com o cabeçalho na segunda linha
    df = pd.read_excel(caminho_arquivo, sheet_name=p_sheet_name, header=p_header)

    # Obter os nomes originais das colunas
    colunas_originais = df.columns.tolist()
    print("Colunas originais:")
    print(colunas_originais)

    # Tratar os nomes das colunas
    colunas_tratadas = [
        unidecode(coluna.strip().lower().replace(" ", "_").replace("+", "mais")) for coluna in colunas_originais
    ]
    print("\nColunas tratadas:")
    print(colunas_tratadas)

    # Atualizar o DataFrame com os nomes tratados
    df.columns = colunas_tratadas

    return df


# Inicializar o cliente BigQuery
client = bigquery.Client()

# Função para gravar o DataFrame no BigQuery
def salvar_no_bigquery(df, dataset_id, tabela_id, project_id):

    tabela_completa = f"{dataset_id}.{tabela_id}"
    
    try:
        # Enviar para o BigQuery usando pandas_gbq.to_gbq
        to_gbq(
            df, 
            tabela_completa, 
            project_id=project_id, 
            if_exists="replace"  # Substitui a tabela, ajuste para "append" se necessário
        )
        print(f"DataFrame salvo com sucesso na tabela {tabela_completa}.")
    except Exception as e:
        print(f"Erro ao salvar o DataFrame no BigQuery: {e}")


p_file_path, p_sheet_name, p_header,p_tabela_id = run_ingestion(config_path)

base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir o caminho absoluto para o arquivo
caminho_arquivo = os.path.join(base_dir, p_file_path)
print(f"Diretório atual de execução: {base_dir}")
#print(f"Caminho absoluto do arquivo: {file_path}")

wait_for_file(caminho_arquivo, timeout=60)

df = read_xlsx(caminho_arquivo, p_sheet_name, p_header)
dataset_id = 'mfranco_michael'
project_id = 'ps-eng-dados-ds3x'
salvar_no_bigquery(df, dataset_id, p_tabela_id, project_id)



