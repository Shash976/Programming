from sklearn.model_selection import train_test_split #Splitting your dataset is essential for an unbiased evaluation of prediction performance.
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
"""
filepath = input(r"Filepath: ")
x_name = input("X: ")
y_name = input("Y: ")"""
data = pd.read_excel(r"C:\Users\Sanket Goel\Downloads\Manish_LR.xlsx", header=0)
x = data["ECL Intensity"]
y = data["Glucsoe (mM)"]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

