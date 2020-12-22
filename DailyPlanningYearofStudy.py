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
        df = pd.merge(df_mskills1, df_grades, left_on="Q10_2", right_on="SIS Login ID")
        # "Q2_2_TEXT" -- cleaned midterm survey
        # "Q62_2" -- ms 1
        return df

    Year_of_Study = "Q626"
    Daily_Planning = "Q53"

    df = join_w_grades("cleaned_grades.csv", "cleaned_metaskills_3.csv")
    df = df.merge(df, pd.read_csv("cleaned_metaskills_1.csv"), left_on="Q10_2", right_on="Q62_2")

    
