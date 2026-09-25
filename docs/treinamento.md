# Dados, Pré-processamento e Treinamento

## 1. Dados e Pré-processamento
O projeto utiliza o dataset **`Customer-Churn-Records.csv`**, que engloba dados cadastrais, geográficos e de utilização de produtos por parte dos clientes.

Para garantir a reprodutibilidade e atender aos requisitos do case, os dados processados são armazenados de forma estruturada em diretórios locais (`data/processed/`), sendo os caminhos e versões dos datasets registados diretamente como artefatos no ecossistema do MLflow.

**Etapas principais do pipeline de dados:**
* **Remoção de Identificadores:** Exclusão de colunas que não agregam valor preditivo ou que possam induzir sobreajuste (ex: `RowNumber`, `Surname`, `CustomerId`).
* **Tratamento da Variável Alvo:** Mapeamento da coluna `Exited` (0 para clientes retidos e 1 para evasão/churn).
* **Transformação Categórica:** Codificação de variáveis textuais/categóricas para formato numérico adequado aos algoritmos.
* **Divisão de Dados:** Particionamento do dataset em conjuntos de treino e teste.
* **Balanceamento:** Avaliação e tratamento do desbalanceamento de classes através de técnicas como SMOTE ou NearMiss, quando aplicável.

---

## 2. Algoritmos Utilizados
O pipeline de treino explora e compara diferentes abordagens de classificação para selecionar o modelo com melhor desempenho no problema de churn:
* **Decision Tree**
* **Random Forest**
* **K-Nearest Neighbors (KNN)**

Os modelos são avaliados com base em métricas robustas de classificação: **Acurácia (Accuracy), Precisão (Precision), Revocação (Recall), F1-Score e Matriz de Confusão**, focando especialmente na capacidade de detetar corretamente a classe positiva (churn).

---

## 3. Como Executar o Treinamento

Para executar o pipeline de treino localmente, siga os passos abaixo:

1. Clone o repositório e configure o ambiente virtual:
   ```powershell
   git clone [https://github.com/daniboi123/customer-churn-mlops.git](https://github.com/daniboi123/customer-churn-mlops.git)
   cd customer-churn-mlops
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt



   Certifique-se de que o servidor do MLflow está ativo e execute o script principal de treino:

PowerShell
$env:MLFLOW_TRACKING_URI="[http://127.0.0.1:5000](http://127.0.0.1:5000)"
python src/training/train_mlflow.py