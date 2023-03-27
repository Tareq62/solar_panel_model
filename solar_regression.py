import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime

# import solar panel data for The Bronx, NY (full year of 2006) and split Date and Time into new columns
df = pd.read_csv('/Users/tareq/solar_panel_model/ny-pv-2006/Actual_40.85_-73.85_2006_DPV_21MW_5_Min.csv')
df['LocalTime'] = pd.to_datetime(df['LocalTime']) 
df['Date'] = df['LocalTime'].dt.date
df['Time'] = df['LocalTime'].dt.time

# group DataFrame by Date, taking sum of all power generated each day and resulting in only 365 rows
df2 = df.groupby('Date').sum('Power(MW)').reset_index()

# import DataFrame of parsed weather features (TempF, TempK, Humidity, HrsDaylight) for the corresponding 365 days of 2006
features_df = pd.read_csv('/Users/tareq/solar_panel_model/Bronx_Weather_2006.csv')

# merge the two DataFrames including solar panel power and weather features and clean up the types
merge_df = df2.merge(features_df,
                  on ='Date', how='right')
merge_df['Power(MW)'] = df2['Power(MW)']
merge_df = merge_df.drop(['Date', 'TempF'],axis=1)
merge_df = merge_df.astype({'TempK':'float', 'Humidity':'float', 'HrsDaylight':'float'})

# create feature variables for regression
X = merge_df.drop('Power(MW)', axis=1)
y = merge_df['Power(MW)'].to_numpy().reshape(-1, 1)

# create train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1) #random_state=101)

# fit the LinearRegression model on the train set
model = LinearRegression()
model.fit(X_train, y_train)

# predict solar power generated on the days that were part of the test set based on known weather data
predictions = model.predict(X_test)
#for prediction in predictions:
#    prediction = round(prediction, 1)

#print('Predicted values (MW):')
#print(predictions)

#print('Actual values (MW):')
#print(y_test)

print('Predicted values (MW):  | Actual values (MW):')
for value in range(len(predictions)):
    print(f'         {predictions[value]} | {y_test[value]}')


# model evaluation
print('mean_squared_error : ', round(mean_squared_error(y_test, predictions), 2))
print('mean_absolute_error : ', round(mean_absolute_error(y_test, predictions), 2))

# coefficients
coefficients = pd.concat([pd.DataFrame(X.columns),pd.DataFrame(np.transpose(model.coef_))], axis=1, ignore_index=True)
coefficients.rename(columns={0: 'Feature:', 1: 'Coefficient:'}, inplace=True)
print(coefficients)