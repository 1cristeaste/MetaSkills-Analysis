import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # this backend only renders PNGs

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
        list = (df[Year_of_Study])
        for i in list:
            if i == year:
                count += 1
        return count


    Year_of_Study = "Q626"
    Stress_Intervention = "Q58.1"

    df = join_w_grades("Data/cleaned_grades.csv",
                       "Data/cleaned_metaskills_1.csv")
    df = pd.merge(df, pd.read_csv("Data/cleaned_metaskills_3.csv"),
                  left_on="Q62_2", right_on="Q10_2")

    Liked_Stress_Intervention = df.loc[
        (df[Stress_Intervention] == "Strongly agree") |
        (df[Stress_Intervention] == "Slightly agree") |
        (df[Stress_Intervention] == "Mostly agree") |
        (df[Stress_Intervention] == "Somewhat agree")]

    Disliked_Stress_Intervention = df.loc[
        (df[Stress_Intervention] == "Strongly disagree") |
        (df[Stress_Intervention] == "Slightly disagree") |
        (df[Stress_Intervention] == "Mostly disagree") |
        (df[Stress_Intervention] == "Somewhat disagree")]

    Neither_Stress_Intervention = df.loc[
        (df[Stress_Intervention] == "Neither agree nor disagree")]

    labels = [1, 2, 3, 4, 5]
    Liked_Years = [count_years(Liked_Stress_Intervention, "1st year"),
                   count_years(Liked_Stress_Intervention, "2nd year"),
                   count_years(Liked_Stress_Intervention, "3rd year"),
                   count_years(Liked_Stress_Intervention, "4th year"),
                   count_years(Liked_Stress_Intervention, "5th or more year")]

    Disliked_Years = [count_years(Disliked_Stress_Intervention, "1st year"),
                      count_years(Disliked_Stress_Intervention, "2nd year"),
                      count_years(Disliked_Stress_Intervention, "3rd year"),
                      count_years(Disliked_Stress_Intervention, "4th year"),
                      count_years(Disliked_Stress_Intervention,
                                  "5th or more year")]

    Neither_Years = [count_years(Neither_Stress_Intervention, "1st year"),
                     count_years(Neither_Stress_Intervention, "2nd year"),
                     count_years(Neither_Stress_Intervention, "3rd year"),
                     count_years(Neither_Stress_Intervention, "4th year"),
                     count_years(Neither_Stress_Intervention,
                                 "5th or more year")]

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
    rects1 = ax.bar(x - width * 1.2, Liked_Years, width, label='Liked')
    rects2 = ax.bar(x + width * 1.2, Disliked_Years, width, label='Disliked')
    rects3 = ax.bar(x, Neither_Years, width, label="Neither")

    ax.set_ylabel('')
    ax.set_title('Year LikedDisliked Proportion')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig("Year LikedDisliked Proportion")
