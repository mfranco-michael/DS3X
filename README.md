# DS3X

Este repositório contém a implementação de um pipeline de ingestão e processamento de dados utilizando Python e Docker. O objetivo principal é automatizar a ingestão de dados de diferentes fontes, realizar operações de transformação e salvar os resultados no BigQuery.

## Estrutura do Projeto

```
DS3X/
├── data/                             # Diretório para armazenar arquivos de dados
│   ├── raw/                          # Dados brutos ingeridos
├── src/                              # Código-fonte principal
│   ├── ingestion.py                  # Script de ingestão de dados
│   ├── rawdata_bigquery.py           # Script para processar dados e salvar no BigQuery
│   ├── trusted.py                    # Script para para criar a tabela trusted
│   ├── configs/                      # Configurações para diferentes ingestões
│       ├── icf.json                  # Parametros para o arquivo ICC
│       ├── icc_rawdata_bigquery.json # Parametros para o rawdata ICC (bigquery)
        ├── icf.json                  # Parametros para o arquivo ICF
        ├── icf_rawdata_bigquery.json # Parametros para o rawdata ICC (bigquery)
├── Dockerfile                        # Configuração do Docker
├── docker-compose.yml                # Orquestração de containers Docker
├── requirements.txt                  # Dependências Python
└── README.md                         # Documentação do projeto
```

## Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Conta no Google Cloud e um arquivo de credenciais do Service Account (`SA-michael.json`).

## Instalação

1. **Clone o Repositório**:

   ```bash
   git clone git@github.com:mfranco-michael/DS3X.git
   cd DS3X
   ```

2. **Configure o Arquivo de Credenciais**:

   Coloque o arquivo `SA-michael.json` no diretório raiz do projeto.

   Adicione o nome do arquivo ao `.gitignore` para evitar upload acidental:

   ```bash
   echo "SA-michael.json" >> .gitignore
   ```

3. **Instale as Dependências Locais (Opcional)**:

   Se quiser rodar os scripts localmente, use o `pip` para instalar as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Construir e Executar com Docker Compose**:

   Para construir as imagens e rodar os containers:

   ```bash
   docker-compose up --build
   ```

   Os seguintes serviços serão executados:

   - **ICF**: Ingestão de dados para o arquivo ICF.
   - **ICC**: Ingestão de dados para o arquivo ICC.
   - **RawData BigQuery**: Processamento e upload dos dados para o BigQuery.
   - **Trusted**: Roda um ctas da tabela trusted no BigQuery.

2. **Logs e Debug**:

   Os logs dos serviços podem ser visualizados diretamente no terminal ou inspecionados individualmente:

   ```bash
   docker logs <nome_do_container>
   ```

3. **Parar os Containers**:

   Para parar e remover os containers:

   ```bash
   docker-compose down
   ```

## Configuração do BigQuery

Certifique-se de que:

1. A tabela de destino no BigQuery existe ou está configurada para ser criada automaticamente.
2. O arquivo `SA-michael.json` contém as permissões necessárias para gravar nos datasets configurados.

## Estrutura dos Scripts

### **ingestion.py**

Este script realiza a ingestão de dados de fontes configuradas em arquivos `.json`. Ele salva os dados ingeridos como arquivos `.xlsx` no diretório `data/raw`.

### **rawdata_bigquery.py**

Processa os arquivos `.xlsx` da pasta `data/raw`, sobe no BigQuery.

### **trusted.py**

Realiza operações como joins e salva o resultado final no BigQuery.

