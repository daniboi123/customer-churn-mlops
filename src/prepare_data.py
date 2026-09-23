import argparse
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split


TARGET = "inadimplente"


def gerar_base_credito(n=6000, random_state=42):
   rng = np.random.default_rng(random_state)

   idade = rng.integers(18, 70, size=n)
   renda_mensal = rng.lognormal(mean=8.2, sigma=0.55, size=n)
   tempo_emprego_anos = rng.gamma(shape=2.0, scale=2.0, size=n)
   score_interno = rng.normal(loc=620, scale=90, size=n).clip(300, 900)
   valor_solicitado = rng.lognormal(mean=9.2, sigma=0.65, size=n)
   num_parcelas = rng.choice([6, 12, 18, 24, 36, 48], size=n)
   tipo_renda = rng.choice(
       ["CLT", "autonomo", "servidor_publico", "aposentado"],
       p=[0.55, 0.25, 0.15, 0.05],
       size=n,
   )
   possui_restricao = rng.choice(["sim", "nao"], p=[0.14, 0.86], size=n)

   risco = (
       -3.0
       - 0.006 * (score_interno - 600)
       - 0.00005 * (renda_mensal - 4000)
       + 0.00004 * (valor_solicitado - 10000)
       + 0.35 * (possui_restricao == "sim")
       + 0.18 * (tipo_renda == "autonomo")
       - 0.03 * tempo_emprego_anos
   )

   prob = 1 / (1 + np.exp(-risco))
   inadimplente = rng.binomial(1, prob)

   return pd.DataFrame(
       {
           "idade": idade,
           "renda_mensal": renda_mensal.round(2),
           "tempo_emprego_anos": tempo_emprego_anos.round(1),
           "score_interno": score_interno.round(0),
           "valor_solicitado": valor_solicitado.round(2),
           "num_parcelas": num_parcelas,
           "tipo_renda": tipo_renda,
           "possui_restricao": possui_restricao,
           "inadimplente": inadimplente,
       }
   )


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("--n-samples", type=int, default=6000)
   parser.add_argument("--test-size", type=float, default=0.25)
   parser.add_argument("--random-state", type=int, default=42)
   parser.add_argument("--output-dir", type=str, default="data/processed")
   parser.add_argument("--pipeline-id", type=str, default="manual")
   args = parser.parse_args()

   base_output_dir = Path(args.output_dir)
   output_dir = base_output_dir / args.pipeline_id
   output_dir.mkdir(parents=True, exist_ok=True)

   df = gerar_base_credito(
       n=args.n_samples,
       random_state=args.random_state,
   )

   X = df.drop(columns=[TARGET])
   y = df[TARGET]

   train_df, test_df = train_test_split(
       df,
       test_size=args.test_size,
       stratify=y,
       random_state=args.random_state,
   )

   train_path = output_dir / "train.csv"
   test_path = output_dir / "test.csv"
   full_path = output_dir / "full.csv"

   train_df.to_csv(train_path, index=False)
   test_df.to_csv(test_path, index=False)
   df.to_csv(full_path, index=False)

   with mlflow.start_run():
       mlflow.log_params(
           {
                "step": "prepare",
                "n_samples": args.n_samples,
                "test_size": args.test_size,
                "random_state": args.random_state,
                "pipeline_id": args.pipeline_id,
                "base_output_dir": str(base_output_dir),
                "output_dir_final": str(output_dir),
           }
       )

       mlflow.log_metrics(
           {
               "n_train": len(train_df),
               "n_test": len(test_df),
               "target_rate_full": float(df[TARGET].mean()),
               "target_rate_train": float(train_df[TARGET].mean()),
               "target_rate_test": float(test_df[TARGET].mean()),
           }
       )

       mlflow.set_tags(
           {
               "project": "risco_credito",
            #    "course_lesson": "aula_09",
               "pipeline_step": "prepare",
           }
       )

       mlflow.log_artifact(str(full_path), artifact_path="data")
       mlflow.log_artifact(str(train_path), artifact_path="data")
       mlflow.log_artifact(str(test_path), artifact_path="data")

   print(f"Dados salvos em: {output_dir}")


if __name__ == "__main__":
   main()
