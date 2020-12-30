import pandas as pd
import matplotlib
from matplotlib.mathtext import List

matplotlib.use("Agg")  # this backend only renders PNGs
import matplotlib.pyplot as plt
from scipy.stats import shapiro, mannwhitneyu, \
    ttest_ind  # tests null hypothesis if its normally distributed
from statsmodels.graphics.gofplots import qqplot_2samples
import statsmodels.api as sm

if __name__ == "__main__":

    def join_w_grades(grades_filepath: str,
                      metaskills_resp_filepath: str) -> pd.DataFrame:
        df_grades = pd.read_csv(grades_filepath)
        df_mskills1 = pd.read_csv(metaskills_resp_filepath)
        df = pd.merge(df_mskills1, df_grades, left_on="Q62_2",
                      right_on="SIS Login ID")
        return df

    Year_of_Study = "Q626"
    Daily_Planning = "Q58"

    df = join_w_grades("Data/cleaned_grades.csv",
                       "Data/cleaned_metaskills_1.csv")
    df = pd.merge(df, pd.read_csv("Data/cleaned_metaskills_3.csv"),
                  left_on="Q62_2", right_on="Q10_2")

    Liked_Daily_Planning = df.loc[(df[Daily_Planning] == "Strongly agree") |
                                  (df[Daily_Planning] == "Slightly agree") |
                                  (df[Daily_Planning] == "Mostly agree") |
                                  (df[Daily_Planning] == "Somewhat agree")]

    Disliked_Daily_Planning = df.loc[
        (df[Daily_Planning] == "Strongly disagree") |
        (df[Daily_Planning] == "Slightly disagree") |
        (df[Daily_Planning] == "Mostly disagree") |
        (df[Daily_Planning] == "Somewhat disagree")]

    fig = df.plot.bar(x=Year_of_Study)

    '''fig = plt.figure()
    fig.bar(Liked_Daily_Planning[Year_of_Study])
    fig.bar(Disliked_Daily_Planning[Year_of_Study] + 0.25)
    fig.savefig("Plots/YearofStudy DailyPlanning")'''

