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
        # "Q62_2" -- ms 1
        return df

    Growth_Question = "Q100"
    df = join_w_grades("Data/cleaned_grades.csv",
                       "Data/cleaned_metaskills_1.csv")

    Disliked_Growth = df.loc[(df[Growth_Question] == "Strongly Disagree") |
                          (df[Growth_Question] == "Mostly Disagree") |
                          (df[Growth_Question] == "Somewhat Disagree") |
                          (df[Growth_Question] == "Slightly Disagree")]

    Liked_Growth = df.loc[(df[Growth_Question] == "Strongly Agree") |
                          (df[Growth_Question] == "Mostly Agree") |
                          (df[Growth_Question] == "Somewhat Agree") |
                          (df[Growth_Question] == "Slightly Agree")]

    grades_Disliked_Growth = Disliked_Growth["Midterm Current Score"]
    grades_Disliked_Growth = grades_Disliked_Growth.dropna()
    grades_Liked_Growth = Liked_Growth["Midterm Current Score"]
    grades_Liked_Growth = grades_Liked_Growth.dropna()

    print(mannwhitneyu(grades_Liked_Growth, grades_Disliked_Growth))
    print("Num of Students who Liked the Growth Intervention")
    print(len(grades_Liked_Growth))
    print("Num of Students who disliked the Growth Intervention")
    print(len(grades_Disliked_Growth))

    plt.hist(x=grades_Liked_Growth, density=True, label="Liked the Growth Intervention", alpha=0.3)
    plt.hist(x=grades_Disliked_Growth, density=True, label="Disliked the Growth Intervention", alpha=0.3)
    plt.legend()
    plt.savefig("LikedDisliked Growth Intervention.png")


