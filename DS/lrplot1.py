import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd


data = pd.read_excel(r"C:\Users\Sanket Goel\Downloads\Manish_LR.xlsx", header=0)
x = data["ECL Intensity"]
y = data["Glucsoe (mM)"]
slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()