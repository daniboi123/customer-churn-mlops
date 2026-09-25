# Arquitetura Técnica e da Solução

## 1. Visão Geral da Arquitetura
A arquitetura foi desenvolvida de forma modular para separar claramente as responsabilidades de cada etapa do ciclo de vida de Machine Learning, garantindo manutenibilidade, rastreabilidade e facilidade de deploy.

**Fluxo Geral (End-to-End):**
1. **Dados Brutos:** Dataset `Customer-Churn-Records.csv`.
2. **Processamento:** Limpeza, remoção de colunas irrelevantes e pré-processamento.
3. **Treino de ML:** Avaliação comparativa de algoritmos (Decision Tree, Random Forest, KNN, XGBoost).
4. **MLflow Tracking & Registry:** Registo de parâmetros, métricas, artefatos e versionamento do modelo campeão.
5. **Contentorização:** Empacotamento do modelo versionado utilizando Docker.
6. **Serving / API:** Disponibilização de um endpoint HTTP para inferência em tempo real.

---

## 2. Componentes Tecnológicos

| Componente | Tecnologia | Responsabilidade |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem base para toda a lógica da solução |
| **Machine Learning** | Scikit-learn| Treino, otimização e avaliação dos modelos preditivos |
| **Experiment Tracking** | MLflow | Registo centralizado de parâmetros, métricas e artefatos de treino |
| **Model Registry** | MLflow | Gestão do ciclo de vida, aprovação e versionamento dos modelos |
| **Serving** | MLflow Model Serving | Disponibilização do modelo treinado em formato de API |
| **Contentorização** | Docker | Empacotamento da aplicação e do modelo para execução consistente |
| **Orquestração** | Scripts Modulares em Python | Organização estruturada e sequencial das etapas do pipeline |
| **Persistência de Dados** | Sistema de Ficheiros Local + MLflow | Armazenamento estruturado dos datasets (`data/processed/`) com rastreabilidade de artefatos integrada ao MLflow |

---

