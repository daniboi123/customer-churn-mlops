import argparse
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.metrics import (
   classification_report,
   confusion_matrix,
   f1_score,
   precision_score,
   recall_score,
   roc_auc_score,
)


TARGET = "inadimplente"


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("--model-uri", type=str, required=True)
   parser.add_argument("--data-dir", type=str, required=True)
   parser.add_argument("--threshold", type=float, default=0.5)
   parser.add_argument("--pipeline-id", type=str, default="manual")
   args = parser.parse_args()

   data_dir = Path(args.data_dir)
   test_df = pd.read_csv(data_dir / "test.csv")

   X_test = test_df.drop(columns=[TARGET])
   y_test = test_df[TARGET]

   model = mlflow.sklearn.load_model(args.model_uri)

   y_proba = model.predict_proba(X_test)[:, 1]
   y_pred = (y_proba >= args.threshold).astype(int)

   report_text = classification_report(
       y_test,
       y_pred,
       target_names=["adimplente", "inadimplente"],
   )

   report_dict = classification_report(
       y_test,
       y_pred,
       target_names=["adimplente", "inadimplente"],
       output_dict=True,
   )

   cm = confusion_matrix(y_test, y_pred)
   tn, fp, fn, tp = cm.ravel()

   with mlflow.start_run():
       mlflow.log_params(
           {
                "step": "evaluate",
                "eval_data_dir_resolved": str(data_dir),
           }
       )

       mlflow.log_metrics(
           {
               "roc_auc_teste": float(roc_auc_score(y_test, y_proba)),
               "precision_inadimplente": float(
                   precision_score(y_test, y_pred, zero_division=0)
               ),
               "recall_inadimplente": float(
                   recall_score(y_test, y_pred, zero_division=0)
               ),
               "f1_inadimplente": float(
                   f1_score(y_test, y_pred, zero_division=0)
               ),
               "tn": int(tn),
               "fp": int(fp),
               "fn": int(fn),
               "tp": int(tp),
           }
       )

       mlflow.set_tags(
           {
               "project": "risco_credito",
            #    "course_lesson": "aula_09",
               "pipeline_step": "evaluate",
               "pipeline_id": args.pipeline_id,
           }
       )

       mlflow.log_text(report_text, "reports/classification_report.txt")
       mlflow.log_dict(report_dict, "reports/classification_report.json")

   print(report_text)


if __name__ == "__main__":
   main()
