Gestão de Experimentos e Rastreabilidade com MLflow
1. Visão geral

O MLflow é a ferramenta central de MLOps utilizada neste projeto.

Ele é responsável por:

Rastreamento de experimentos (tracking);

Registro de parâmetros;

Registro de métricas;

Armazenamento de artefatos;

Registro e versionamento dos modelos;

Disponibilização dos modelos para inferência (Model Serving).

Cada execução do pipeline pode registrar informações como:

Hiperparâmetros utilizados;

Métricas de avaliação;

Artefatos do modelo;

Relatórios de classificação;

Informações relacionadas ao dataset utilizado;

Modelo registrado no Model Registry.

2. Pré-requisitos

Antes de executar o MLflow, certifique-se de que os seguintes componentes estão instalados:

Git;

Python 3.11;

MLflow;

Dependências do projeto.

O projeto utiliza Python 3.11, conforme definido no arquivo python_env.yaml.

Importante: este projeto não utiliza requirements.txt. As dependências são instaladas de acordo com o python_env.yaml.

3. Configuração inicial em uma máquina nova

Se você acabou de clonar o repositório, siga os passos abaixo.

3.1 Clonar o repositório
git clone https://github.com/daniboi123/customer-churn-mlops.git
cd customer-churn-mlops

3.2 Criar o ambiente virtual

No Windows:

py -3.11 -m venv .venv


Ative o ambiente:

.\.venv\Scripts\Activate.ps1


Depois confirme:

python --version


O resultado esperado é:

Python 3.11.x

3.3 Caso o PowerShell bloqueie a ativação

Se aparecer uma mensagem informando que a execução de scripts está desabilitada, execute:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


Depois tente novamente:

.\.venv\Scripts\Activate.ps1

3.4 Atualizar as ferramentas de instalação

Com o ambiente virtual ativado:

python -m pip install --upgrade pip setuptools wheel

3.5 Instalar as dependências

Instale as dependências utilizadas pelo projeto:

python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests


Valide a instalação:

mlflow --version


Também é possível executar:

python -c "import mlflow, pandas, numpy, sklearn, matplotlib, cloudpickle, requests; print('Dependências instaladas com sucesso!')"

4. Configuração do MLflow Tracking Server
4.1 Criar um banco novo

Cada máquina que executar o projeto deve possuir seu próprio banco local do MLflow.

Para evitar problemas com bancos antigos ou schemas incompatíveis entre versões do MLflow, o banco utilizado nesta configuração fica dentro da pasta:

mlflow_data/


Crie a pasta:

New-Item -ItemType Directory -Force .\mlflow_data

4.2 Inicializar o banco do MLflow

Execute:

mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"


Esse comando cria/atualiza o schema do banco utilizado pelo MLflow.

A estrutura ficará semelhante a:

customer-churn-mlops/
│
├── mlflow_data/
│   └── mlflow.db
│
└── ...


Importante: não é necessário utilizar os arquivos mlflow.db ou mlflow_registry.db que eventualmente estejam presentes no repositório. A configuração deste guia utiliza um banco novo em mlflow_data/mlflow.db.

5. Iniciar o MLflow Tracking Server

Abra um terminal PowerShell com o ambiente virtual ativado.

Execute:

mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000


Se tudo estiver correto, o servidor será iniciado localmente.

A interface web ficará disponível em:

http://127.0.0.1:5000


Abra esse endereço no navegador.

Importante: mantenha esse terminal aberto enquanto estiver executando os experimentos.

6. Configurar o Tracking URI

Abra um segundo terminal PowerShell.

Entre novamente no projeto:

cd caminho\para\customer-churn-mlops


Ative o ambiente:

.\.venv\Scripts\Activate.ps1


Configure a URI do servidor MLflow:

$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"


Confirme:

echo $env:MLFLOW_TRACKING_URI


O resultado esperado é:

http://127.0.0.1:5000


Essa variável de ambiente é válida apenas para o terminal atual. Caso um novo terminal seja aberto, execute novamente o comando.

7. Executar o Pipeline

O projeto possui um pipeline configurado no arquivo MLproject.

O pipeline realiza as etapas de:

Preparação dos dados
        ↓
Treinamento
        ↓
Avaliação
        ↓
Registro do modelo

7.1 Executar diretamente pelo Python

Para executar o pipeline:

python src/run_pipeline.py `
    --model-name random_forest `
    --n-samples 6000 `
    --test-size 0.25 `
    --random-state 42 `
    --threshold 0.5 `
    --registered-model-name customer_churn_model

8. Executar através do MLflow Projects

Também é possível executar o pipeline utilizando o MLproject.

Execute:

mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local


O parâmetro:

--env-manager local


informa ao MLflow para utilizar o ambiente virtual atual, evitando que ele tente criar outro ambiente Python.

9. Executar outros modelos

Caso o código do projeto possua outros algoritmos implementados, o parâmetro model_name pode ser alterado.

Por exemplo:

mlflow run . -e pipeline `
    -P model_name=logistic_regression `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local


Os valores aceitos para model_name dependem dos modelos implementados em:

src/train.py

10. Visualizar os experimentos

Enquanto o Tracking Server estiver executando, abra:

http://127.0.0.1:5000


Na interface do MLflow será possível visualizar:

Experimentos;

Runs;

Parâmetros;

Métricas;

Artefatos;

Modelos registrados.

O fluxo de rastreabilidade é:

Experiment
    ↓
Run
    ↓
Parâmetros + Métricas
    ↓
Artefatos
    ↓
Modelo
    ↓
Model Registry

11. Model Registry

O pipeline registra o modelo utilizando o nome informado no parâmetro:

registered_model_name


Por exemplo:

customer_churn_model


Após a execução, o modelo poderá ser visualizado na área de Models do MLflow.

12. Model Serving

Depois que o modelo estiver registrado, ele pode ser disponibilizado para inferência utilizando o MLflow Model Serving.

Por exemplo:

mlflow models serve `
    -m "models:/customer_churn_model/1" `
    -p 5001 `
    --host 127.0.0.1 `
    --env-manager local


O servidor de inferência ficará disponível em:

http://127.0.0.1:5001


O número:

/1


representa a versão do modelo registrada no Model Registry.

Caso exista outra versão, substitua o número correspondente:

models:/customer_churn_model/2

13. Estrutura recomendada para execução

Para facilitar a execução, recomenda-se utilizar dois terminais.

Terminal 1 — MLflow Server
.\.venv\Scripts\Activate.ps1

mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000

Terminal 2 — Pipeline
.\.venv\Scripts\Activate.ps1

$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"

mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local

14. Solução de problemas
Erro: requirements.txt não encontrado

Este projeto não utiliza requirements.txt.

Utilize:

python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests

Erro: execução de scripts bloqueada no PowerShell

Execute:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


Depois:

.\.venv\Scripts\Activate.ps1

Erro: Detected out-of-date database schema

Esse erro normalmente ocorre quando um banco MLflow criado por uma versão anterior do MLflow é utilizado com uma versão mais recente.

Para uma instalação nova, utilize o banco dedicado:

mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"


e inicie o servidor apontando explicitamente para ele:

mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000

15. Resumo rápido

Depois de clonar o projeto, a sequência completa é:

git clone https://github.com/daniboi123/customer-churn-mlops.git
cd customer-churn-mlops

py -3.11 -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests

New-Item -ItemType Directory -Force .\mlflow_data

mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"


Depois, em um terminal:

mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000


E em outro terminal:

.\.venv\Scripts\Activate.ps1

$env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"

mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local


A interface do MLflow estará disponível em:

http://127.0.0.1:5000
