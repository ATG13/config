import pandas as pd
import numpy as np

df = pd.read_csv("/home/atg/Aadi/Christ College Notes/5) Neural Networks and Deep Learning/customer-churn-rate/data/bank_churn_data.csv")

X = df.drop(columns=["CustomerId", "Surname", "Exited"], axis=1)
y = df['Excited']

print(X.head())