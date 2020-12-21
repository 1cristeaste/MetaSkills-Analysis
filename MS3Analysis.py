import pandas as pd
from scipy.stats import shapiro  #tests null hypothesis if its normally distributed

if __name__ == "__main__":
    def join_w_grades(grades_filepath: str, metaskills_resp_filepath: str) -> pd.DataFrame:
        df_grades = pd.read_csv(grades_filepath)
        df_mskills1 = pd.read_csv(metaskills_resp_filepath)
        df = pd.merge(df_mskills1, df_grades, left_on="Q10_2", right_on="SIS Login ID")
        return df


    df = join_w_grades("cleaned_grades.csv", "cleaned_metaskills_3.csv")
    Show_CBT = df.loc[df["showcbt"] == "yes"]
    No_Show_CBT = df.loc[df["showcbt"] == "no"]
    Grades_Received_CBT = Show_CBT["Midterm Current Score"]
    Grades_Received_CBT = Grades_Received_CBT.dropna()

    print(Show_CBT)
    print(No_Show_CBT)
    print(shapiro(Grades_Received_CBT))



