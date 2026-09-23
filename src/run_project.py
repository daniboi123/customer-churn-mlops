import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

submitted_run = mlflow.run(
   uri=".",
   entry_point="pipeline",
   parameters={
       "model_name": "random_forest",
       "n_samples": 6000,
       "test_size": 0.25,
       "random_state": 42,
       "threshold": 0.5,
       "registered_model_name": "risco_credito_project_model",
   },
   experiment_name="risco_credito/09_mlflow_projects",
   env_manager="local",
   synchronous=True,
)

print("Run ID:", submitted_run.run_id)
