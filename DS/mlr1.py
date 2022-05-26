import numpy as np
import statsmodels.api as sm
import numpy as np
import pandas as pd
import sys

df = pd.get_dummies(pd.read_excel(r"C:\Users\Sanket Goel\Downloads\Manish_MLR.xlsx"), drop_first=True)

x = df[['Voltage (V)', 'Luminol (mM)', "H2O2(mM)", "PBS (M)", "Fingers", "GOx(mg/mL)"]]
y = df['Average']

X = sm.add_constant(x)
model = sm.OLS(y, x).fit()
print(model.predict(x))