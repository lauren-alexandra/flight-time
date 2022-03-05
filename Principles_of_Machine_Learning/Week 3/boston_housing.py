"""
Title: Simple Linear Regression in Scikit Learn
Description: The model predicts the value of a house using the features given in the Boston housing dataset.
"""
print("Loading housing prices model...")

import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

df = pd.DataFrame(data)
features = df.rename({0: 'CRIM', 1: 'ZN', 2: 'INDUS', 3: 'CHAS', 4: 'NOX', 5: 'RM', 6: 'AGE', 7: 'DIS', 8: 'RAD', 9: 'TAX', 10: 'PTRATIO', 11: 'B', 12: 'LSTAT'}, axis=1)

train_x, test_x, train_y, test_y = train_test_split(features, target, test_size=0.2, random_state=30)

lr = LinearRegression()
lr.fit(train_x, train_y)
predictions = lr.predict(test_x)

predictions = ["{:.2f}".format(pred) for pred in predictions]
test_y = ["{:.2f}".format(price) for price in test_y]

print("\nReal Price of House #1: ", test_y[0])
print("Predicted Price of House #1: ", predictions[0])

print("\nReal Price of House #2: ", test_y[1])
print("Predicted Price of House #2: ", predictions[1])

print("\nReal Price of House #3: ", test_y[2])
print("Predicted Price of House #3: ", predictions[2])

time.sleep(10)
