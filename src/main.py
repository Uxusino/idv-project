import pandas as pd

PATH = "./data/omophobia.csv"

df = pd.read_csv(PATH, encoding='latin-1')
print(df.head())