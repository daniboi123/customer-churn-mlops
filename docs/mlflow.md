Aqui está o conteúdo atualizado e completo para o ficheiro **`docs/mlflow.md`**, incorporando todos os comandos exatos de inicialização, configuração da Tracking URI, execução via MLflow Projects (com parâmetros de exemplo) e o comando de *serving* adaptado para o contexto de **Customer Churn**:

---

### `docs/mlflow.md`

```markdown
# Gestão de Experiências e Rastreabilidade com MLflow

## 1. Controlo do Ciclo de Vida
O MLflow é a ferramenta central de MLOps adotada neste projeto. Cada execução (*run*) do pipeline de treino submete automaticamente para o servidor de *tracking* um conjunto completo de informações, incluindo:
* Hiperparâmetros utilizados;
* Métricas de avaliação de desempenho (*metrics*);
* Artefatos do modelo treinado e relatórios de classificação;
* O registo do dataset consumido naquela execução específica.

---

## 2. Iniciar o MLflow Tracking Server

Para acompanhar os experimentos através da interface gráfica, abra um terminal dedicado e execute os seguintes passos:

1. **Defina a Tracking URI antes de iniciar o servidor:**
   ```powershell
   $env:MLFLOW_TRACKING_URI="[http://127.0.0.1:5000](http://127.0.0.1:5000)"

   $env:MLFLOW_TRACKING_URI="http://127.0.0.1:5000"

```

2. **Inicie o servidor localmente** (utilizando SQLite como backend store e a pasta local para os artefatos):
```powershell
mlflow server `
--backend-store-uri sqlite:///mlflow.db `
--default-artifact-root ./mlartifacts `
--host 127.0.0.1 `
--port 5000

```



Após a inicialização, a interface web do MLflow ficará acessível em: `http://127.0.0.1:5000`.

---

## 3. Execução de Treinamento via MLflow Projects

O projeto suporta a execução parametrizada através de MLflow Projects. Com o Tracking URI devidamente configurado num segundo terminal, pode disparar o treino de diferentes algoritmos alterando o parâmetro `model_name` e o nome do modelo registado (`registered_model_name`):

* **Exemplo com Random Forest:** A seguir a duas alternativa de execução um via python e via power shell:
```
python:

python src/run_pipeline.py --model-name random_forest --n-samples 6000 --test-size 0.25 --random-state 42 --threshold 0.5 --registered-model-name customer_churn_model


powershell:
mlflow run . -e pipeline `
-P model_name=random_forest `
-P n_samples=6000 `
-P test_size=0.25 `
-P random_state=42 `
-P threshold=0.5 `
-P registered_model_name=customer_churn_model `
--env-manager local `
--experiment-name "customer_churn/mlflow_projects"

```



* **Exemplo com outro algoritmo (ex: Regressão Logística ):**

```

python src/run_pipeline.py --model-name logistic_regression --n-samples 6000 --test-size 0.25 --random-state 42 --threshold 0.5 --registered-model-name customer_churn_model




powershell
mlflow run . -e pipeline `
-P model_name=logistic_regression `
-P n_samples=6000 `
-P test_size=0.25 `
-P random_state=42 `
-P threshold=0.5 `
-P registered_model_name=customer_churn_model `
--env-manager local `
--experiment-name "customer_churn/mlflow_projects"




```


*(Nota: Pode alternar o algoritmo ajustando o argumento `-P model_name=` conforme os estimadores suportados no código do projeto).*

---

## 4. Serving do Modelo Registado

Após o registo do modelo no *Model Registry*, este pode ser colocado a responder a pedidos de inferência através do comando de *serving* do MLflow:

```powershell
mlflow models serve `
-m models:/customer_churn_model/1 `
-p 5001 `
--host 127.0.0.1 `
--env-manager local

```

python src/run_pipeline.py --model-name random_forest --n-samples 6000 --test-size 0.25 --random-state 42 --threshold 0.5 --registered-model-name customer_churn_model

*(Dica: Caso necessite de testar outra versão ou nome de modelo, basta alterar o caminho em `-m models:/<NOME_DO_MODELO>/<VERSAO>`).*

---

## 5. Model Registry e Rastreabilidade

Após a comparação de desempenho na interface do MLflow, o modelo selecionado é promovido para o **Model Registry**.

Esta funcionalidade garante a rastreabilidade total de ponta a ponta:
`Experiência (Experiment) → Execução (Run) → Hiperparâmetros e Métricas → Artefatos → Modelo Registado → Versão → Deployment`

```

```