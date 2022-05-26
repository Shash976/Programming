import numpy as np
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

df = pd.read_excel(r"C:\Users\Sanket Goel\Downloads\Manish_MLR.xlsx")

x = df[['Voltage (V)', 'Luminol (mM)', "H2O2(mM)", "PBS (M)", "Fingers", "GOx(mg/mL)"]]
y = df['Average']

model = LinearRegression().fit(x, y)
print(model.predict(x))