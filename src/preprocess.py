import pandas as pd
import numpy as np

OMOPHOBIA = "./data/omophobia.csv"
EU = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic",
      "Germany", "Denmark", "Estonia", "Greece", "Spain",
      "Finland", "France", "Croatia", "Hungary", "Ireland",
      "Italy", "Lithuania", "Luxembourg", "Latvia", "Malta",
      "Netherlands", "Poland", "Portugal", "Romania", "Sweden",
      "Slovenia", "Slovakia", "United Kingdom"]

def get_law_data() -> pd.DataFrame:
    df = pd.read_csv(OMOPHOBIA)
    df = df[df["COUNTRY"].isin(EU)]
    df.drop(columns=["Unnamed: 14", "Unnamed: 15", "MAX PENALTY", "DATE OF DECRIM", "CSSSA LEGAL?"], inplace=True)
    df.replace(["YES", "LIMITED", "NO"], [2, 1, 0], inplace=True)
    return df

def sum_laws(df: pd.DataFrame, values: list) -> pd.DataFrame:
    df_summable = df.drop(columns=["COUNTRY"])[values]
    df2 = df_summable.copy()
    df2["Sum"] = pd.to_numeric(df_summable.sum(axis = 1), errors='coerce')
    df2["COUNTRY"] = df["COUNTRY"]
    return df2