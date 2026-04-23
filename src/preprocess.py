import pandas as pd
import numpy as np

OMOPHOBIA = "./data/omophobia.csv"

SURVEY_VIOLENCE = "./data/LGBT_Survey_ViolenceAndHarassment.csv"
SURVEY_DAILY = "./data/LGBT_Survey_DailyLife.csv"
SURVEY_DISCRIMINATION = "./data/LGBT_Survey_Discrimination.csv"
SURVEY_RIGHTS = "./data/LGBT_Survey_RightsAwareness.csv"

SURVEYS = {
    SURVEY_DAILY: "Daily life",
    SURVEY_DISCRIMINATION: "Discrimination",
    SURVEY_RIGHTS: "Rights awareness",
    SURVEY_VIOLENCE: "Violence and harrasment"
}

QUESTION_FIXES = {
    "open_at_work": "Have you been open about you being L, G, B or T at work?",
    "open_at_school": "Have you been open about you being L, G, B or T at school?"
}

NUMERICAL_ANSWERS = ["g5"]

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

def get_questions(survey: str) -> dict:
    df = pd.read_csv(survey)

    keys = df["question_code"].unique()
    #print(keys)
    values2 = []
    for k in keys:
        if k in QUESTION_FIXES.keys():
            v = QUESTION_FIXES[k]
            values2.append(v)
            continue

        v = df[df["question_code"] == k].iloc[0]
        v = v["question_label"]
        values2.append(v)

    questions = dict(zip(keys, values2))

    return questions

def question_results(survey: str, question: str, country: str) -> pd.DataFrame:
    df = pd.read_csv(survey)
    df["percentage"] = pd.to_numeric(df["percentage"], errors="coerce")
    df = df[df["CountryCode"] == country]
    answers_df = df[df["question_code"] == question]

    if question in NUMERICAL_ANSWERS:
        answers_df["answer"] = pd.to_numeric(answers_df["answer"], errors="coerce")
    return answers_df