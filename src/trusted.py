from google.cloud import bigquery
import os
import time

time.sleep(7)

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


# Inicializar o cliente BigQuery
client = bigquery.Client()

# Query SQL
query = """
CREATE OR REPLACE TABLE ps-eng-dados-ds3x.mfranco_michael.icf_icc_refined AS
SELECT 
    FORMAT_DATETIME('%Y-%m', icc.mes) mes,
    icc.icc icc_indice,
    ROUND(((icc.icc - LAG(icc.icc) OVER (ORDER BY icc.mes)) / LAG(icc.icc) OVER (ORDER BY icc.mes)) * 100, 2) AS icc_variacao,
    icf.icf icf_indice,
    ROUND(((icf.icf - LAG(icf.icf) OVER (ORDER BY icf.icf)) / LAG(icf.icf) OVER (ORDER BY icf.mes)) * 100, 2) AS icf_variacao,
    FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', CURRENT_TIMESTAMP()) load_timestamp
FROM `ps-eng-dados-ds3x.mfranco_michael.icc_raw_dados_do_icc` icc
INNER JOIN `ps-eng-dados-ds3x.mfranco_michael.icf_raw_dados_do_icf` icf
ON icc.mes = icf.mes
"""

# Executar a query
query_job = client.query(query)

# Esperar a conclusão da execução
query_job.result()

print("Query executada com sucesso e a tabela foi criada/atualizada!")
