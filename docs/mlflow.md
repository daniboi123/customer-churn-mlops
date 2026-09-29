

```markdown
# Gestão de Experimentos e Rastreabilidade com MLflow

## 1. Visão Geral
O **MLflow** é a ferramenta central de MLOps utilizada neste projeto. Ele é responsável por:
* Rastreamento de experimentos (tracking);
* Registro de parâmetros;
* Registro de métricas;
* Armazenamento de artefatos;
* Registro e versionamento dos modelos;
* Disponibilização dos modelos para inferência (Model Serving).

Cada execução do pipeline pode registrar informações como:
* Hiperparâmetros utilizados;
* Métricas de avaliação;
* Artefatos do modelo;
* Relatórios de classificação;
* Informações relacionadas ao dataset utilizado;
* Modelo registrado no Model Registry.

---

## 2. Pré-requisitos
Antes de executar o MLflow, certifique-se de que os seguintes componentes estão instalados:
* Git;
* Python 3.11;
* MLflow;
* Dependências do projeto.

*Importante:* Este projeto não utiliza `requirements.txt`. As dependências são instaladas de acordo com o `python_env.yaml`.

---

## 3. Configuração Inicial em uma Máquina Nova
Se acabou de clonar o repositório, siga os passos abaixo.

### 3.1 Clonar o repositório
```powershell
git clone [https://github.com/daniboi123/customer-churn-mlops.git](https://github.com/daniboi123/customer-churn-mlops.git)
cd customer-churn-mlops

```

### 3.2 Criar o ambiente virtual

No Windows:

```powershell
py -3.11 -m venv .venv

```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1

```

Confirme a versão:

```powershell
python --version

```

*O resultado esperado é:* `Python 3.11.x`

### 3.3 Caso o PowerShell bloqueie a ativação

Se aparecer uma mensagem informando que a execução de scripts está desabilitada, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

Depois tente novamente:

```powershell
.\.venv\Scripts\Activate.ps1

```

### 3.4 Atualizar as ferramentas de instalação

Com o ambiente virtual ativado:

```powershell
python -m pip install --upgrade pip setuptools wheel

```

### 3.5 Instalar as dependências

```powershell
python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests

```

Valide a instalação:

```powershell
mlflow --version

```

Ou execute:

```powershell
python -c "import mlflow, pandas, numpy, sklearn, matplotlib, cloudpickle, requests; print('Dependências instaladas com sucesso!')"

```

---

## 4. Configuração do MLflow Tracking Server

### 4.1 Criar um banco novo

Cada máquina que executar o projeto deve possuir seu próprio banco local do MLflow. Para evitar problemas com bancos antigos, o banco utilizado fica dentro da pasta `mlflow_data/`. Crie a pasta:

```powershell
New-Item -ItemType Directory -Force .\mlflow_data

```

### 4.2 Inicializar o banco do MLflow

Execute:

```powershell
mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"

```

*Importante:* Não é necessário utilizar os arquivos `mlflow.db` ou `mlflow_registry.db` antigos que eventualmente estejam no repositório.

---

## 5. Iniciar o MLflow Tracking Server

Abra um terminal PowerShell com o ambiente virtual ativado e execute:

```powershell
mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000

```

* A interface web ficará disponível em: `http://127.0.0.1:5000`
* **Importante:** Mantenha esse terminal aberto enquanto estiver executando os experimentos.

---

## 6. Configurar o Tracking URI

Abra um segundo terminal PowerShell, entre no projeto e ative o ambiente:

```powershell
cd caminho\para\customer-churn-mlops
.\.venv\Scripts\Activate.ps1

```

Configure a URI do servidor MLflow:

```powershell
$env:MLFLOW_TRACKING_URI="[http://127.0.0.1:5000](http://127.0.0.1:5000)"

```

Confirme:

```powershell
echo $env:MLFLOW_TRACKING_URI

```

---

## 7. Executar o Pipeline

O pipeline realiza as etapas de: **Preparação dos dados $\rightarrow$ Treinamento $\rightarrow$ Avaliação $\rightarrow$ Registro do modelo**.

### 7.1 Executar diretamente pelo Python

```powershell
python src/run_pipeline.py `
    --model-name random_forest `
    --n-samples 6000 `
    --test-size 0.25 `
    --random-state 42 `
    --threshold 0.5 `
    --registered-model-name customer_churn_model

```

---

## 8. Executar através do MLproject

Também é possível executar utilizando o MLproject:

```powershell
mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local

```

*O parâmetro `--env-manager local` informa ao MLflow para utilizar o ambiente virtual atual.*

---

## 9. Executar outros modelos

Para testar outros algoritmos implementados, altere o parâmetro `model_name`:

```powershell
mlflow run . -e pipeline `
    -P model_name=logistic_regression `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local

```

---

## 10. Visualizar os experimentos

Abra `http://127.0.0.1:5000`. O fluxo de rastreabilidade é:

`Experiment` $\rightarrow$ `Run` $\rightarrow$ `Parâmetros + Métricas` $\rightarrow$ `Artefatos` $\rightarrow$ `Modelo` $\rightarrow$ `Model Registry`

---

## 11. Model Registry

O pipeline registra o modelo utilizando o nome informado no parâmetro `registered_model_name` (ex: `customer_churn_model`). Após a execução, o modelo fica visível na aba **Models** do MLflow.

---

## 12. Model Serving

Para disponibilizar o modelo registrado para inferência:

```powershell
mlflow models serve `
    -m "models:/customer_churn_model/1" `
    -p 5001 `
    --host 127.0.0.1 `
    --env-manager local

```

* O servidor ficará disponível em: `http://127.0.0.1:5001`
* O `/1` representa a versão do modelo.

---

## 13. Estrutura recomendada para execução (Dois Terminais)

### Terminal 1 — MLflow Server

```powershell
.\.venv\Scripts\Activate.ps1

mlflow server `
    --backend-store-uri "sqlite:///./mlflow_data/mlflow.db" `
    --default-artifact-root "./mlflow_data/artifacts" `
    --host 127.0.0.1 `
    --port 5000

```

### Terminal 2 — Pipeline

```powershell
.\.venv\Scripts\Activate.ps1

$env:MLFLOW_TRACKING_URI="[http://127.0.0.1:5000](http://127.0.0.1:5000)"

mlflow run . -e pipeline `
    -P model_name=random_forest `
    -P n_samples=6000 `
    -P test_size=0.25 `
    -P random_state=42 `
    -P threshold=0.5 `
    -P registered_model_name=customer_churn_model `
    --env-manager local

```

---

## 14. Solução de problemas

* **Erro: requirements.txt não encontrado** $\rightarrow$ Instale as dependências manualmente via pip (Seção 3.5).
* **Erro: execução de scripts bloqueada no PowerShell** $\rightarrow$ Execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
* **Erro: Detected out-of-date database schema** $\rightarrow$ Utilize `mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"`.

---

## 15. Resumo rápido

Sequência completa pós-clonagem:

```powershell
git clone [https://github.com/daniboi123/customer-churn-mlops.git](https://github.com/daniboi123/customer-churn-mlops.git)
cd customer-churn-mlops

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel
python -m pip install mlflow pandas numpy scikit-learn matplotlib cloudpickle requests

New-Item -ItemType Directory -Force .\mlflow_data
mlflow db upgrade "sqlite:///./mlflow_data/mlflow.db"

```

* **No Terminal 1:** Correr o comando `mlflow server ...`
* **No Terminal 2:** Ativar a env, definir a variável de ambiente e correr o `mlflow run ...`.

```

```
