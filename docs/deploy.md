# Deployment, Contentorização e Inferência

## 1. Serving do Modelo
Uma vez que o modelo esteja devidamente registado no MLflow, o mesmo pode ser disponibilizado para inferência através de um servidor dedicado integrado à ferramenta, escutando por padrão na porta `5001`.

---

## 2. Contentorização com Docker
Para garantir que o modelo seja executado em um ambiente isolado, reprodutível e idêntico ao de homologação/produção, a solução utiliza a geração automática de imagens Docker via MLflow.

**Passo a passo para gerar e executar o contentor:**

1. Defina a variável de ambiente com o URI do modelo registado:
   ```powershell
   $env:MODEL_URI="models:/<NOME_DO_MODELO>/<VERSAO>"





Construa a imagem Docker através do CLI do MLflow:

PowerShell
mlflow models build-docker `
--model-uri $env:MODEL_URI `
--name "customer-churn-serving:latest"
Execute o contentor localmente mapeando a porta de acesso:

PowerShell
docker run -d `
  --name customer-churn-container `
  -p 5001:8080 `
  customer-churn-serving:latest
3. Testando a API de Inferência
Após iniciar o contentor, pode validar o funcionamento do servidor de inferência:

Verificação de saúde (Healthcheck):

PowerShell
curl.exe [http://127.0.0.1:5001/ping](http://127.0.0.1:5001/ping)
(Resposta esperada: OK)

Envio de Requisição de Inferência (Payload):
As predições são efetuadas enviando os dados do cliente no formato JSON para o endpoint de invocação:

HTTP
POST [http://127.0.0.1:5001/invocations](http://127.0.0.1:5001/invocations)
4. Observabilidade
Na versão atual, o ecossistema do MLflow monitora de forma robusta o comportamento do treino e do modelo. Os registos de execução da API podem ser inspecionados diretamente via logs do Docker (docker logs customer-churn-container).

A integração de ferramentas avançadas de monitorização em tempo real (como Prometheus e Grafana) para tracking de data drift e model drift está documentada no projeto como uma melhoria futura planeada.