import pandas as pd
import matplotlib
from matplotlib.mathtext import List

matplotlib.use("Agg") #this backend only renders PNGs
import matplotlib.pyplot as plt
from scipy.stats import shapiro, mannwhitneyu, ttest_ind  #tests null hypothesis if its normally distributed
from statsmodels.graphics.gofplots import qqplot_2samples
import statsmodels.api as sm

if __name__ == "__main__":
    def join_w_grades(grades_filepath: str, metaskills_resp_filepath: str) -> pd.DataFrame:
        df_grades = pd.read_csv(grades_filepath)
        df_mskills1 = pd.read_csv(metaskills_resp_filepath)
        df = pd.merge(df_mskills1, df_grades, left_on="Q62_2", right_on="SIS Login ID")
        # "Q2_2_TEXT" -- cleaned midterm survey
        # "Q62_2" -- midterm survey 1
        return df

    midterm_question = "Q222"

    df = join_w_grades("Data/cleaned_grades.csv",
                       "Data/cleaned_metaskills_1.csv")
    df_Midterm_Survey = pd.read_csv("Data/cleaned_midterm_survey.csv")
    df_MS_Grades = pd.merge(df, df_Midterm_Survey, left_on="Q62_2", right_on="Q2_2_TEXT")

    guessed_PCRS_Agree = df_MS_Grades.loc[(df_MS_Grades[midterm_question] == "7-Strongly agree") |
                                        (df_MS_Grades[midterm_question] == "6-Agree") |
                                        (df_MS_Grades[midterm_question] == "5-Somewhat agree")]

    guessed_PCRS_Disagree = df_MS_Grades.loc[(df_MS_Grades[midterm_question] == "1-Strongly disagree") |
                                    (df_MS_Grades[midterm_question] == "2-Disagree") |
                                    (df_MS_Grades[midterm_question] == "3-Somewhat disagree")]

    Agree_PCRS_Show_Exam = guessed_PCRS_Agree.loc[guessed_PCRS_Agree["showdailyplan"] == "yes"]
    Agree_PCRS_No_Show_Exam = guessed_PCRS_Agree.loc[guessed_PCRS_Agree["showdailyplan"] == "no"]

    Disagree_PCRS_Show_Exam = guessed_PCRS_Disagree.loc[guessed_PCRS_Disagree["showdailyplan"] == "yes"]
    Disagree_PCRS_No_Show_Exam = guessed_PCRS_Disagree.loc[guessed_PCRS_Disagree["showdailyplan"] == "no"]

    grades_Agree_Show = Agree_PCRS_Show_Exam["Midterm Current Score"]
    grades_Agree_Show = grades_Agree_Show.dropna()

    grades_Agree_No_Show = Agree_PCRS_No_Show_Exam["Midterm Current Score"]
    grades_Agree_No_Show = grades_Agree_No_Show.dropna()

    grades_Disagree_Show = Disagree_PCRS_Show_Exam["Midterm Current Score"]
    grades_Disagree_Show = grades_Disagree_Show.dropna()

    grades_Disagree_No_Show = Disagree_PCRS_No_Show_Exam["Midterm Current Score"]
    grades_Disagree_No_Show = grades_Disagree_No_Show.dropna()

    print("Students who Agree that they guess")
    print(mannwhitneyu(grades_Agree_Show, grades_Agree_No_Show))
    print("Students who Disagree with guessing")
    print(mannwhitneyu(grades_Disagree_Show, grades_Disagree_No_Show))
    print("Num Grades Agree Show")
    print(len(grades_Agree_Show))
    print("Num Grades Agree No Show")
    print(len(grades_Agree_No_Show))
    print("Num Grades Disagree Show")
    print(len(grades_Disagree_Show))
    print("Num Grades Disagree No Show")
    print(len(grades_Disagree_No_Show))


    plt.hist(x=grades_Disagree_Show, density=True, label="Received daily planning intervention", alpha=0.3)
    plt.hist(x=grades_Disagree_No_Show, density=True, label="No daily planning intervention", alpha=0.3)
    plt.title("Students who disagreed that they guess")
    plt.legend()
    plt.savefig("Disagreed_Daily_Planning")

