import pandas as pd
import matplotlib
from matplotlib.mathtext import List

matplotlib.use("Agg") #this backend only renders PNGs
import matplotlib.pyplot as plt
from scipy.stats import shapiro, mannwhitneyu, ttest_ind  #tests null hypothesis if its normally distributed
from statsmodels.graphics.gofplots import qqplot_2samples
import statsmodels.api as sm

if __name__ == "__main__":
    def make_qqplot(x: List, y: List) -> None:
        plt_x = sm.ProbPlot(x)
        plt_y = sm.ProbPlot(y)
        qqplot_2samples(plt_x, plt_y)
        plt.savefig("testing")

    def join_w_grades(grades_filepath: str, metaskills_resp_filepath: str) -> pd.DataFrame:
        df_grades = pd.read_csv(grades_filepath)
        df_mskills1 = pd.read_csv(metaskills_resp_filepath)
        df = pd.merge(df_mskills1, df_grades, left_on="Q62_2", right_on="SIS Login ID")
        return df


    df = join_w_grades("cleaned_grades.csv", "cleaned_metaskills_1.csv")
    # Choosing to disregard the "Neither Agree nor Disagree" section since they
    # don't seem to have an opinion
    Show_Strongly_Agree = df.loc[(df["Q124"] == "Strongly Agree") |
                                 (df["Q124"] == "Mostly Agree") |
                                 (df["Q124"] == "Somewhat Agree") |
                                 (df["Q124"] == "Slightly Agree")]
    Show_Strongly_Disagree = df.loc[(df["Q124"] == "Strongly Disagree") |
                                    (df["Q124"] == "Mostly Disagree") |
                                    (df["Q124"] == "Somewhat Disagree") |
                                    (df["Q124"] == "Slightly Disagree")]

    Grades_Strongly_Agree = Show_Strongly_Agree["Midterm Current Score"]
    Grades_Strongly_Disagree = Show_Strongly_Disagree["Midterm Current Score"]

    print(mannwhitneyu(Grades_Strongly_Agree, Grades_Strongly_Disagree))
    #print(make_qqplot(Grades_Strongly_Agree, Grades_Strongly_Disagree))
    #print(shapiro(Grades))
    #print(mannwhitneyu())
    plt.hist(x=Grades_Strongly_Agree, density=True, label="Agreed Metaskills were helpful", alpha=0.3)
    plt.hist(x=Grades_Strongly_Disagree, density=True, label="Disagreed Metaskills were helpful", alpha=0.3)
    plt.legend()
    plt.savefig("hist.png")


