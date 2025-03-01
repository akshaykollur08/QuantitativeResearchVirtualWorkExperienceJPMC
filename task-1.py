# Author: Akshay Kollur
# Task One for JPMorgan Chase & Co. Quantitative Research Virtual Work Experience

# Various imports to be used for data visualization, extrapolation, mathematics, machine learning, and linear modeling
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates



# Variables for parsing the natural gas csv file
# data in the Nat_Gas.csv file, with dates and prices
gas_price_data = pd.read_csv('Nat_Gas.csv', parse_dates=['Dates'])

gas_price_data['Prices'] = pd.to_numeric(gas_price_data['Prices'], errors='coerce')



# Help to visiualize the historical natural gas prices and dates
# over time
plt.figure(figsize=(10,6), num="Natural Gas Prices Over Time")
plt.plot(gas_price_data["Dates"], gas_price_data["Prices"], label="Natural Gas Prices Over Time")

# Plot's title, x-label, y-label, legend, and various
# other components for the Natural Gas Prices Over Time plot
plt.title("Natural Gas Prices Over Time (Monthly)")
plt.xlabel("Dates")
plt.ylabel("Price (USD per unit)")
plt.xticks(rotation=45)

# Formatting the date on the x-axis to make it easily readable
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))

# Automatically prevents plot features from being cut off
plt.tight_layout()

plt.grid(True)

plt.legend()

plt.show()

# Start the extrapolation and data transformation process

# Convert the "Dates" to the number of days since the first recorded date for linear regression
gas_price_data["Days_Since_Start"] = (gas_price_data["Dates"] - gas_price_data["Dates"].min()).dt.days

# Prepare the features (Days since start) and target (Price) for the linear regression model
x_features = gas_price_data[["Days_Since_Start"]]  
# Target: Prices for the stock
y_features = gas_price_data["Prices"]  

# Initialize and fit the Linear Regression model
linear_regression_model = LinearRegression()
linear_regression_model.fit(x_features, y_features)



# Generate the next 12 months (in days) for future price prediction\
# Predicting 12 months ahead as to account for the ability of the program to predict a stock price a year in the future as per project specification
future_days = np.array([gas_price_data["Days_Since_Start"].max() + i * 30 for i in range(1, 13)]) 
future_dates = pd.date_range(gas_price_data["Dates"].max(), periods=12, freq='ME') 
# to_datetime(), pd.to_timedelta(future_days, unit="D")
predicted_prices = linear_regression_model.predict(future_days.reshape(-1, 1))

# Plot the historical data and the extrapolated future prices
plt.figure(figsize=(10, 6), num="Natural Gas Price Forecast (For Next 12 Months)")
plt.plot(gas_price_data["Dates"], gas_price_data["Prices"], label="Historical Natural Gas Prices")
plt.plot(future_dates, predicted_prices, label="Predicted Prices (For Next 12 months)", linestyle=":")

# Customize the plot
plt.title("Natural Gas Price Forecast (For Next 12 Months)")
plt.xlabel("Date")
plt.ylabel("Price (USD per unit)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Display the plot
plt.show()


# Given a date, check the extrapolation data and cross reference, then utilize that price data to predict price for that date
# Can be a 1 year in the future date inputted or a past date.
# Returns a price in USD
def price_prediction_from_date(date):
    
    # Convert the input argument date into a datetime standard
    date = pd.to_datetime(date)
    
    # Calculate and determine the number of days since the start date
    days_since_start_date = (date-gas_price_data["Dates"].min()).days
    
    # Predict the price from the linear regression model that predicts the prices
    # from the numpy array of the days since the start date
    predicted_price = linear_regression_model.predict(pd.DataFrame([[days_since_start_date]]))
    
    # returns that first entry in that predicted prices array 
    return predicted_price[0]


date = '2025-02-25'
predicted_price = price_prediction_from_date(date)
print(predicted_price)

