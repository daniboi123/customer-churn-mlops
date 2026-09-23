import argparse
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
   accuracy_score,
   f1_score,
   precision_score,
   recall_score,
   roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


TARGET = "inadimplente"

NUM_COLS = [
   "idade",
   "renda_mensal",
   "tempo_emprego_anos",
   "score_interno",
   "valor_solicitado",
   "num_parcelas",
]

CAT_COLS = ["tipo_renda", "possui_restricao"]


def make_preprocess():
   numeric_pipe = Pipeline(
       steps=[
           ("imputer", SimpleImputer(strategy="median")),
           ("scaler", StandardScaler()),
       ]
   )

   categorical_pipe = Pipeline(
       steps=[
           ("imputer", SimpleImputer(strategy="most_frequent")),
           ("onehot", OneHotEncoder(handle_unknown="ignore")),
       ]
   )

   return ColumnTransformer(
       transformers=[
           ("num", numeric_pipe, NUM_COLS),
           ("cat", categorical_pipe, CAT_COLS),
       ]
   )


def build_estimator(model_name, random_state):
   if model_name == "logistic_regression":
       return LogisticRegression(
           max_iter=2000,
           class_weight="balanced",
           random_state=random_state,
       )

   if model_name == "decision_tree":
       return DecisionTreeClassifier(
           max_depth=5,
           min_samples_leaf=50,
           class_weight="balanced",
           random_state=random_state,
       )

   if model_name == "random_forest":
       return RandomForestClassifier(
           n_estimators=100,
           max_depth=8,
           min_samples_leaf=20,
           class_weight="balanced",
           n_jobs=-1,
           random_state=random_state,
       )

   raise ValueError(f"Modelo não reconhecido: {model_name}")


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("--model-name", type=str, default="random_forest")
   parser.add_argument("--data-dir", type=str, required=True)
   parser.add_argument("--random-state", type=int, default=42)
   parser.add_argument(
       "--registered-model-name",
       type=str,
       default="risco_credito_project_model",
   )
   parser.add_argument("--pipeline-id", type=str, default="manual")
   args = parser.parse_args()

   data_dir = Path(args.data_dir)
   train_df = pd.read_csv(data_dir / "train.csv")
   test_df = pd.read_csv(data_dir / "test.csv")

   X_train = train_df.drop(columns=[TARGET])
   y_train = train_df[TARGET]

   X_test = test_df.drop(columns=[TARGET])
   y_test = test_df[TARGET]

   model_pipe = Pipeline(
       steps=[
           ("prep", make_preprocess()),
           (
               "model",
               build_estimator(
                   model_name=args.model_name,
                   random_state=args.random_state,
               ),
           ),
       ]
   )

   with mlflow.start_run() as run:
       model_pipe.fit(X_train, y_train)

       y_pred = model_pipe.predict(X_test)
       y_proba = model_pipe.predict_proba(X_test)[:, 1]

       metrics = {
           "roc_auc_teste": float(roc_auc_score(y_test, y_proba)),
           "accuracy_teste": float(accuracy_score(y_test, y_pred)),
           "precision_inadimplente": float(
               precision_score(y_test, y_pred, zero_division=0)
           ),
           "recall_inadimplente": float(
               recall_score(y_test, y_pred, zero_division=0)
           ),
           "f1_inadimplente": float(
               f1_score(y_test, y_pred, zero_division=0)
           ),
       }

       mlflow.log_params(
           {
                "step": "train",
                "train_data_dir_resolved": str(data_dir),
           }
       )

       mlflow.log_metrics(metrics)

       mlflow.set_tags(
           {
               "project": "risco_credito",
            #    "course_lesson": "aula_09",
               "pipeline_step": "train",
               "pipeline_id": args.pipeline_id,
           }
       )

       input_example = X_train.head(5).copy()
       signature = infer_signature(
           input_example,
           model_pipe.predict(input_example),
       )

       model_info = mlflow.sklearn.log_model(
           sk_model=model_pipe,
           name="model",
           signature=signature,
           input_example=input_example,
           registered_model_name=args.registered_model_name,
           skops_trusted_types=["numpy.dtype"],
       )

       mlflow.log_param("model_uri", model_info.model_uri)

       print("Run ID:", run.info.run_id)
       print("Model URI:", model_info.model_uri)
       print("Métricas:", metrics)


if __name__ == "__main__":
   main()
