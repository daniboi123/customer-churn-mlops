import argparse
import uuid

import mlflow

from mlflow.tracking import MlflowClient


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("--model-name", type=str, default="random_forest")
   parser.add_argument("--n-samples", type=int, default=6000)
   parser.add_argument("--test-size", type=float, default=0.25)
   parser.add_argument("--random-state", type=int, default=42)
   parser.add_argument("--threshold", type=float, default=0.5)
   parser.add_argument(
       "--registered-model-name",
       type=str,
       default="risco_credito_project_model",
   )
   args = parser.parse_args()

   client = MlflowClient() 

   pipeline_id = f"run_{uuid.uuid4().hex[:8]}"
    #   pipeline_id = f"aula09_{uuid.uuid4().hex[:8]}"
   data_dir = f"data/processed/{pipeline_id}"
#   mlflow.set_experiment("risco_credito/09_mlflow_projects")
   mlflow.set_experiment("risco_credito/mlflow_projects")

   with mlflow.start_run(run_name=f"pipeline_{pipeline_id}") as parent_run:
       parent_run_id = parent_run.info.run_id

       mlflow.log_params(
           {
               "pipeline_id": pipeline_id,
               "model_name": args.model_name,
               "n_samples": args.n_samples,
               "test_size": args.test_size,
               "random_state": args.random_state,
               "threshold": args.threshold,
               "registered_model_name": args.registered_model_name,
           }
       )

       mlflow.set_tags(
           {
               "project": "risco_credito",
            #    "course_lesson": "aula_09",
               "pipeline_step": "orchestrator",
               "run_purpose": "reproducible_pipeline",
           }
       )

       prepare_run = mlflow.run(
           ".",
           entry_point="prepare",
           parameters={
               "n_samples": args.n_samples,
               "test_size": args.test_size,
               "random_state": args.random_state,
               "output_dir": "data/processed",
               "pipeline_id": pipeline_id,
           },
           env_manager="local",
           experiment_name="risco_credito/mlflow_projects",
           synchronous=True,
       )

       train_run = mlflow.run(
           ".",
           entry_point="train",
           parameters={
               "model_name": args.model_name,
               "data_dir": data_dir,
               "random_state": args.random_state,
               "registered_model_name": args.registered_model_name,
               "pipeline_id": pipeline_id,
           },
           env_manager="local",
           experiment_name="risco_credito/mlflow_projects",
           synchronous=True,
       )

       train_data = client.get_run(train_run.run_id)
       model_uri = train_data.data.params["model_uri"]

       evaluate_run = mlflow.run(
           ".",
           entry_point="evaluate",
           parameters={
               "model_uri": model_uri,
               "data_dir": data_dir,
               "threshold": args.threshold,
               "pipeline_id": pipeline_id,
           },
           env_manager="local",
        #    experiment_name="risco_credito/09_mlflow_projects",
           experiment_name="risco_credito/mlflow_projects",
           synchronous=True,
       )

       mlflow.log_params(
           {
               "prepare_run_id": prepare_run.run_id,
               "train_run_id": train_run.run_id,
               "evaluate_run_id": evaluate_run.run_id,
               "model_uri": model_uri,
           }
       )

       mlflow.log_text(
           f"""
# Resumo do pipeline

- Pipeline ID: {pipeline_id}
- Prepare run ID: {prepare_run.run_id}
- Train run ID: {train_run.run_id}
- Evaluate run ID: {evaluate_run.run_id}
- Model URI: {model_uri}
""",
           "reports/pipeline_summary.md",
       )

       print("Pipeline ID:", pipeline_id)
       print("Parent run ID:", parent_run_id)
       print("Prepare run ID:", prepare_run.run_id)
       print("Train run ID:", train_run.run_id)
       print("Evaluate run ID:", evaluate_run.run_id)
       print("Model URI:", model_uri)


if __name__ == "__main__":
   main()
