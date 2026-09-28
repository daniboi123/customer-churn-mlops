Customer Churn MLOps

Solução de Engenharia de Machine Learning desenvolvida para o case de certificação, com foco no gerenciamento do ciclo de vida de modelos de Machine Learning em um cenário de previsão de Customer Churn.

O projeto demonstra, de ponta a ponta, conceitos de MLOps, incluindo processamento de dados, treinamento de modelos, experimentação, versionamento de modelos, rastreamento de experimentos, orquestração, containerização, disponibilização para inferência e monitoramento.

1. Objetivo do Case

O objetivo deste projeto é desenvolver uma solução de Engenharia de Machine Learning capaz de gerenciar o ciclo de vida de modelos de previsão de evasão de clientes (Customer Churn).

A variável alvo utilizada é:

Exited

0 → cliente permaneceu

1 → cliente deixou a empresa

2. Contexto do Problema

A previsão de churn é um problema de classificação binária focado em identificar clientes com maior probabilidade de abandonar a empresa.

O projeto utiliza o dataset Customer-Churn-Records.csv, analisando características cadastrais, geográficas e de utilização de produtos.

3. Tecnologias Utilizadas

Python 3.11: Linguagem principal de desenvolvimento.

Scikit-learn: Treinamento e avaliação dos modelos de Machine Learning.

MLflow: Rastreamento de experimentos (tracking), armazenamento de parâmetros e métricas, Model Registry e Model Serving.

Pandas e NumPy: Manipulação e processamento dos dados.

Matplotlib: Visualização de dados e resultados.

Cloudpickle: Serialização de objetos Python utilizados pelo projeto.

Requests: Comunicação HTTP utilizada em integrações e testes.

Docker: Containerização para empacotamento e execução consistente do modelo.

Persistência de dados: Arquivos locais estruturados em data/processed/, juntamente com artefatos e informações de rastreamento gerenciados pelo MLflow.

Orquestração: Scripts modulares e pipeline configurados por meio do MLflow Projects.

4. Estrutura do Projeto
MLFlow-master/
│
├── data/
│   └── processed/
│
├── docs/
│
├── mlartifacts/
│
├── mlruns/
│
├── notebooks/
│
├── src/
│   ├── prepare_data.py
│   ├── train.py
│   ├── evaluate.py
│   └── run_pipeline.py
│
├── .gitignore
├── MLproject
├── python_env.yaml
├── mlflow.db
├── mlflow_registry.db
├── README.md
└── teste_request.py

5. Configuração e Instalação do Ambiente

O projeto utiliza Python 3.11, conforme definido no arquivo python_env.yaml.

Passo 1: Clonar o repositório
git clone https://github.com/daniboi123/customer-churn-mlops.git
cd customer-churn-mlops

Passo 2: Verificar o Python 3.11

No Windows, verifique as versões disponíveis:

py -0p


O Python 3.11 deve estar instalado para que o ambiente seja criado de acordo com a configuração do projeto.

Passo 3: Criar o ambiente virtual
py -3.11 -m venv .venv

Passo 4: Ativar o ambiente virtual

No PowerShell:

.\.venv\Scripts\Activate.ps1


Após a ativação, o terminal deverá apresentar o prefixo:

(.venv)


Para confirmar a versão do Python:

python --version


O resultado esperado é semelhante a:

Python 3.11.x

Passo 5: Instalar as ferramentas de build
python -m pip install --upgrade pip setuptools wheel

Passo 6: Instalar as dependências

Este projeto não utiliza requirements.txt. As dependências são definidas no arquivo python_env.yaml.

Para instalar as dependências no ambiente virtual:

python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests


As principais dependências são:

mlflow

pandas

numpy

scikit-learn

matplotlib

cloudpickle

requests

Passo 7: Validar a instalação

Verifique o MLflow:

mlflow --version


Também é possível validar as principais bibliotecas:

python -c "import mlflow, pandas, numpy, sklearn, matplotlib; print('Dependências instaladas com sucesso!')"

6. Execução do Projeto

O projeto utiliza MLflow Projects, com os pontos de entrada definidos no arquivo MLproject.

Os principais entry points são:

prepare

train

evaluate

pipeline

Preparação dos dados

A etapa prepare executa o processamento e preparação dos dados:

mlflow run . -e prepare


Também é possível informar parâmetros:

mlflow run . -e prepare -P n_samples=6000 -P test_size=0.25 -P random_state=42


Os dados processados são armazenados em:

data/processed/

Treinamento

Para executar o treinamento:

mlflow run . -e train


Por padrão, o projeto utiliza o modelo:

random_forest


O treinamento também pode receber parâmetros:

mlflow run . -e train -P model_name=random_forest -P random_state=42


O modelo pode ser registrado no MLflow Model Registry com o nome configurado no MLproject.

Avaliação

A etapa de avaliação recebe o URI do modelo treinado:

mlflow run . -e evaluate -P model_uri=<MODEL_URI>


Também é possível configurar o diretório dos dados e o threshold:

mlflow run . -e evaluate -P model_uri=<MODEL_URI> -P threshold=0.5

Pipeline completo

O projeto também disponibiliza uma etapa de pipeline que executa o fluxo completo por meio do arquivo:

src/run_pipeline.py


Para executar:

mlflow run . -e pipeline


É possível configurar parâmetros:

mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=risco_credito_project_model

7. MLflow

O projeto utiliza o MLflow para rastreamento dos experimentos, armazenamento de métricas e parâmetros, gerenciamento de artefatos e registro dos modelos.

Para iniciar a interface do MLflow localmente:

mlflow ui


Por padrão, a interface pode ser acessada em:

http://127.0.0.1:5000


O projeto também possui arquivos locais relacionados à persistência do MLflow:

mlflow.db
mlflow_registry.db
mlartifacts/
mlruns/

8. Dados e Artefatos

Os dados processados pelo pipeline são armazenados na estrutura:

data/processed/


Os experimentos e artefatos gerados pelo MLflow são armazenados localmente conforme a configuração do projeto.

Essa estrutura permite manter a rastreabilidade entre:

Dados utilizados;

Parâmetros de treinamento;

Métricas;

Artefatos;

Modelos treinados;

Execuções do pipeline.

9. Estado Atual e Limitações

A versão atual atende aos requisitos propostos no case.

Algumas evoluções para cenários corporativos de larga escala estão mapeadas:

CI/CD: O fluxo automatizado via GitHub Actions está desenhado na arquitetura, mas não implementado nesta versão local.

Observabilidade: O MLflow realiza o rastreamento das métricas de treinamento; dashboards dedicados em tempo real utilizando Prometheus e Grafana são considerados evoluções futuras.

Escalabilidade: A API via Docker permite replicação horizontal, com expansão futura planejada para ambientes de orquestração como Kubernetes.

10. Documentação

Para informações detalhadas sobre cada etapa do ciclo de vida de Machine Learning deste projeto, consulte a documentação disponível no diretório docs/.

A documentação está organizada de forma modular, contemplando:

🏗️ Arquitetura Técnica e da Solução: desenho da arquitetura, fluxo end-to-end e decisões de design.

📊 Processamento e Treinamento: detalhes sobre os dados, pré-processamento, algoritmos utilizados e instruções de execução.

🔬 MLflow e Tracking de Experimentos: inicialização do servidor de tracking, execução de projetos parametrizados e gerenciamento do Model Registry.

🚀 Deployment e Inferência: instruções para construção da imagem Docker, execução do container e testes da API de serving.

11. Autor

Daniel Henrique de Amorim Sebastião

Projeto desenvolvido como case de certificação em Engenharia de Machine Learning / MLOps.
