import pandas as pd
import matplotlib
from matplotlib.mathtext import List
import numpy as np

matplotlib.use("Agg")  # this backend only renders PNGs
import matplotlib.pyplot as plt
from scipy.stats import shapiro, mannwhitneyu, \
    ttest_ind  # tests null hypothesis if its normally distributed
from statsmodels.graphics.gofplots import qqplot_2samples
import statsmodels.api as sm

if __name__ == "__main__":

    def join_w_grades(grades_filepath: str,
                      metaskills_resp_filepath: str) -> pd.DataFrame:
        print('running merge')
        df_grades = pd.read_csv(grades_filepath)
        df_mskills1 = pd.read_csv(metaskills_resp_filepath)
        df = pd.merge(df_mskills1, df_grades, left_on="Q62_2",
                      right_on="SIS Login ID")
        return df


    def count_years(df, year):
        count = 0
        list = (df["Q626"])
        for i in list:
            if i == year:
                count += 1
        return count


    Year_of_Study = "Q626"
    Daily_Planning = "Q58"
    print("t1")

    df = join_w_grades("../Data/cleaned_grades.csv",
                       "Data/cleaned_metaskills_1.csv")
    df = pd.merge(df, pd.read_csv("../Data/cleaned_metaskills_3.csv"),
                  left_on="Q62_2", right_on="Q10_2")

    print("t2")
    Liked_Daily_Planning = df.loc[(df[Daily_Planning] == "Strongly agree") |
                                  (df[Daily_Planning] == "Slightly agree") |
                                  (df[Daily_Planning] == "Mostly agree") |
                                  (df[Daily_Planning] == "Somewhat agree")]

    Disliked_Daily_Planning = df.loc[
        (df[Daily_Planning] == "Strongly disagree") |
        (df[Daily_Planning] == "Slightly disagree") |
        (df[Daily_Planning] == "Mostly disagree") |
        (df[Daily_Planning] == "Somewhat disagree")]

    Neither_Daily_Planning = df.loc[
        (df[Daily_Planning] == "Neither agree nor disagree")]

    labels = [1, 2, 3, 4, 5]  # might be 5...
    Liked_Years = [count_years(Liked_Daily_Planning, "1st year"),
                   count_years(Liked_Daily_Planning, "2nd year"),
                   count_years(Liked_Daily_Planning, "3rd year"),
                   count_years(Liked_Daily_Planning, "4th year"),
                   count_years(Liked_Daily_Planning, "5th or more year")]

    Disliked_Years = [count_years(Disliked_Daily_Planning, "1st year"),
                      count_years(Disliked_Daily_Planning, "2nd year"),
                      count_years(Disliked_Daily_Planning, "3rd year"),
                      count_years(Disliked_Daily_Planning, "4th year"),
                      count_years(Disliked_Daily_Planning, "5th or more year")]

    Neither_Years = [count_years(Neither_Daily_Planning, "1st year"),
                     count_years(Neither_Daily_Planning, "2nd year"),
                     count_years(Neither_Daily_Planning, "3rd year"),
                     count_years(Neither_Daily_Planning, "4th year"),
                     count_years(Neither_Daily_Planning, "5th or more year")]

    Total_Students = [count_years(df, "1st year"),
                      count_years(df, "2nd year"),
                      count_years(df, "3rd year"),
                      count_years(df, "4th year"),
                      count_years(df, "5th or more year")]

    print("Likes Years Total", Liked_Years)
    print("Disliked Years Total", Disliked_Years)
    print("Neither Years Total", Neither_Years)
    print("Total Students", Total_Students)

    for i in range(len(Total_Students)):
        Liked_Years[i] = Liked_Years[i] / Total_Students[i]
        Disliked_Years[i] = Disliked_Years[i] / Total_Students[i]
        Neither_Years[i] = Neither_Years[i] / Total_Students[i]


    x = np.arange(len(labels))
    width = 0.2
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width*1.2, Liked_Years, width, label='Liked')
    rects2 = ax.bar(x + width * 1.2, Disliked_Years, width, label='Disliked')
    rects3 = ax.bar(x, Neither_Years, width, label="Neither")

    ax.set_ylabel('')
    ax.set_title('Liked Disliked Year w Neither Prop')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig("Liked Disliked Year w Neither Prop")

    '''fig = plt.figure()
    fig.bar(Liked_Daily_Planning[Year_of_Study])
    fig.bar(Disliked_Daily_Planning[Year_of_Study] + 0.25)
    fig.savefig("Plots/YearofStudy DailyPlanning")'''
