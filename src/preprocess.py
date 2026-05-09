import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OMOPHOBIA = os.path.join(BASE_DIR, "omophobia.csv")

SURVEY_VIOLENCE = os.path.join(BASE_DIR, "LGBT_Survey_ViolenceAndHarassment.csv")
SURVEY_DAILY = os.path.join(BASE_DIR, "LGBT_Survey_DailyLife.csv")
SURVEY_DISCRIMINATION = os.path.join(BASE_DIR, "LGBT_Survey_Discrimination.csv")
SURVEY_RIGHTS = os.path.join(BASE_DIR, "LGBT_Survey_RightsAwareness.csv")
SURVEY_TRANS = os.path.join(BASE_DIR, "LGBT_Survey_TransgenderSpecificQuestions.csv")

SURVEYS = {
    SURVEY_DAILY: "Daily life",
    SURVEY_DISCRIMINATION: "Discrimination",
    SURVEY_RIGHTS: "Rights awareness",
    SURVEY_VIOLENCE: "Violence and harrasment",
    SURVEY_TRANS: "Transgender specific questions"
}

QUESTION_FIXES = {
    "open_at_work": "Have you been open about you being L, G, B or T at work?",
    "open_at_school": "Have you been open about you being L, G, B or T at school?",
    "g4_a": "In the last six months, how often have you been treated with less courtesy because you are or are assumed to be L, G, B or T?",
    "g4_b": "In the last six months, how often have you been treated with less respect because you are or are assumed to be L, G, B or T?",
    "g4_c": "In the last six months, how often have you been received poorer services than others because you are or are assumed to be L, G, B or T?",
    "h15": "In the country where you have moved to, have you or your partner been denied or restricted access to any benefits or services?",
    "c8a_f": "During your employment in the last 5 years, have you experienced unequal treatment with respect to employment conditions or benefits?",
    "f1_a": "In the last 5 years, have you been physically/sexually attacked or threatened with violence at home or elsewhere for any reason?",
    "f1_b": "In the last 5 years, have you been personally harassed by someone or a group in a way that really annoyed, offended or upset you?",
    "tr8_g": "Prove diagnosis of gender dysphoria - What would you have to do to change your official documents to match your preferred gender?",
    "b2_c": "What would allow you to be more comfortable living as a L, G or B person? Public figures openly speaking in support of L, G and B people?",
    "b2_e": "What would allow you to be more comfortable living as a L, G or B person? Training of public servants on the rights of L, G and B people?",
    "b2_d": "What would allow you to be more comfortable living as a L, G or B person? National authorities who promote the rights of L, G and B people?",
    "b2_b": "What would allow you to be more comfortable living as a L, G or B person? Measures implemented at school to respect L, G and B people?",
    "b2_a": "What would allow you to be more comfortable living as a L, G or B person? Anti-discrimination policies at the workplace?",
    "b2_f": "What would allow you to be more comfortable living as a L, G or B person? Better acceptance by religious leaders?",
    "b2_i": "What would allow you to be more comfortable living as a L, G or B person? Recognition of same-sex partnerships across the EU?",
    "b1_g": "In your opinion, how widespread is public figures in politics, business, sports, etc being open about themselves being L, G, B or T?",
    "b2_g": "What would allow you to be more comfortable living as a L, G or B person? The possibility to marry or register a partnership?",
    "h14": "Have you ever moved to an EU country together with your same-sex partner, since you registered your partnership?",
    "b2_h": "What would allow you to be more comfortable living as a L, G or B person? The possibility to foster/adopt children?",
    "b1_h": "In your opinion, how widespread are positive measures to promote respect for the human rights of L, G or B people?",
    "b1_c": "In your opinion, how widespread are expressions of hatred and aversion towards L, G, B or T in public?",
    "b1_a": "In your opinion, how widespread is offensive language about L, G, B or T people by politicians?",
    "b1_d": "In your opinion, how widespread are assaults and harassment against L, G, B or T people?",
    "b1_i": "In your opinion, how widespread are positive measures to promote respect for the human rights of transgender people?",
    "b1_b": "In your opinion, how widespread are casual jokes in everyday life about L, G, B or T people?",
    "g2_a": "In your opinion, how many people know that you are L, G, B or T? Family members?",
    "g3_a": "To how many people among the following groups are you open about yourself being L, G, B or T? Family members?",
    "c9_d": "During your schooling before the age of 18, did you see negative comments or conduct because a peer was perceived to be L, G, B or T?",
    "c8a_d": "During your employment, have you seen negative comments or conduct because a colleague is perceived to be L, G, B or T?",
    "c8a_e": "During your employment, have you experienced a general negative attitude at work against people because they are L, G, B or T?",
    "c9_e": "During your schooling before the age of 18, did you see negative comments or conduct because a teacher was perceived to be L, G, B or T?",
    "c4_k": "During the last 12 months, have you personally felt discriminated against because of being L, G, B or T when showing your ID?",
    "c4_i": "During the last 12 months, have you personally felt discriminated against because of being L, G, B or T in a bank or insurance company?",
    "c4_d": "During the last 12 months, have you personally felt discriminated against because of being L, G, B or T by healthcare personnel?",
    "c4_c": "During the last 12 months, have you personally felt discriminated against because of being L, G, B or T when looking for a house?",
    "fa1_5": "Do you think the LAST incident of attack or threat in the past 12 months happened because you were perceived to be L, G, B or T?",
    "fb1_5": "Do you think the LAST incident of harassment in the past 12 months happened because you were perceived to be L, G, B or T?",
    "fa1_3": "How many times did somebody physically/sexually attack or threaten you with violence in the last 12 months in the EU?",
    "fa2_13": "MOST SERIOUS physical/sexual attack or threat of violence - Did you or anyone else report it to any of the following organisations?",
    "fa1_13": "Did you or anyone else report the last incident of physical/sexual attack or threat of violence to any of the following organisations?"
}
SKIP_QUESTIONS = ["c1_b", "c1_c", "tr3"]
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
    correct_keys = []

    values2 = []
    for k in keys:
        if k in SKIP_QUESTIONS:
            continue

        if k in QUESTION_FIXES.keys():
            v = QUESTION_FIXES[k]
            values2.append(v)
            correct_keys.append(k)
            continue

        v = df[df["question_code"] == k].iloc[0]
        v = v["question_label"]
        correct_keys.append(k)
        values2.append(v)

    questions = dict(zip(correct_keys, values2))

    return questions

def question_results(survey: str, question: str, country: str) -> pd.DataFrame:
    df = pd.read_csv(survey)
    df["percentage"] = pd.to_numeric(df["percentage"], errors="coerce")
    df = df[df["CountryCode"] == country]
    answers_df = df[df["question_code"] == question]

    if question in NUMERICAL_ANSWERS:
        answers_df["answer"] = pd.to_numeric(answers_df["answer"], errors="coerce")

    return answers_df