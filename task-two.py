import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Read the data from the CSV file
gas_price_data = pd.read_csv('Nat_Gas.csv', parse_dates=['Dates'])
gas_price_data['Prices'] = pd.to_numeric(gas_price_data['Prices'], errors='coerce')

# Convert the "Dates" to the number of days since the first recorded date for linear regression
gas_price_data["Days_Since_Start"] = (gas_price_data["Dates"] - gas_price_data["Dates"].min()).dt.days

# Prepare the features (Days since start) and target (Price) for the linear regression model
x_features = gas_price_data[["Days_Since_Start"]]  
y_features = gas_price_data["Prices"]

# Initialize and fit the Linear Regression model
linear_regression_model = LinearRegression()
linear_regression_model.fit(x_features, y_features)

# Predict price for a given date
def price_prediction_from_date(date):
    """
    Predicts the price of natural gas on a specific date using linear regression.

    Parameters:
    - date (str): The date for which to predict the price (format: 'YYYY-MM-DD')

    Returns:
    - float: Predicted price for that date.
    """
    date = pd.to_datetime(date)
    days_since_start_date = (date - gas_price_data["Dates"].min()).days
    predicted_price = linear_regression_model.predict(pd.DataFrame([[days_since_start_date]]))
    return predicted_price[0]

# Function to calculate the cost of gas injected
def calculate_injection_cost(inject_volume, inject_price):
    return inject_volume * inject_price

# Function to calculate the revenue from gas withdrawal
def calculate_withdrawal_revenue(withdraw_volume, withdraw_price):
    return withdraw_volume * withdraw_price

# Function to calculate storage cost (constant storage cost for simplicity)
def calculate_storage_cost(current_storage, storage_costs):
    return current_storage * storage_costs

# Function to calculate the total storage volume after injection
def calculate_injected_volume(current_storage, inject_volume, max_volume):
    inject_volume = min(inject_volume, max_volume - current_storage)
    return current_storage + inject_volume

# Function to calculate the total storage volume after withdrawal
def calculate_withdrawn_volume(current_storage, withdraw_volume):
    return max(0, current_storage - withdraw_volume)

# Function to price the gas contract
def price_gas_contract(injection_dates, withdrawal_dates, injection_rate, withdrawal_rate, max_volume, storage_costs):
    """
    Calculates the value of a gas storage contract using price prediction and given parameters.

    Parameters:
    - injection_dates (list): List of dates for gas injections (in 'YYYY-MM-DD' format).
    - withdrawal_dates (list): List of dates for gas withdrawals (in 'YYYY-MM-DD' format).
    - injection_rate (float): Maximum rate at which gas can be injected per day.
    - withdrawal_rate (float): Maximum rate at which gas can be withdrawn per day.
    - max_volume (float): Maximum storage capacity.
    - storage_costs (float): Cost of storing gas per unit volume per time step.

    Returns:
    - float: The total value of the contract (revenue - cost).
    """
    # Initialize variables for tracking gas volume and financials
    current_storage = 0
    total_cost = 0
    total_revenue = 0
    
    # Process each injection event
    for inject_date_str in injection_dates:
        inject_price = price_prediction_from_date(inject_date_str)
        inject_volume = injection_rate  # Assuming full injection for each day
        # Calculate new storage volume after injection
        current_storage = calculate_injected_volume(current_storage, inject_volume, max_volume)
        # Add the injection cost to the total cost
        total_cost += calculate_injection_cost(inject_volume, inject_price)

    # Process each withdrawal event
    for withdraw_date_str in withdrawal_dates:
        withdraw_price = price_prediction_from_date(withdraw_date_str)
        withdraw_volume = withdrawal_rate  # Assuming full withdrawal for each day
        # Calculate the new storage volume after withdrawal
        current_storage = calculate_withdrawn_volume(current_storage, withdraw_volume)
        # Add the withdrawal revenue to the total revenue
        total_revenue += calculate_withdrawal_revenue(withdraw_volume, withdraw_price)

    # Calculate the storage cost
    total_cost += calculate_storage_cost(current_storage, storage_costs)

    # The contract value is the revenue from withdrawals minus the costs of injections and storage
    contract_value = total_revenue - total_cost
    
    return contract_value

# Test example
injection_dates = ["2023-06-30", "2023-07-31"]
withdrawal_dates = ["2023-08-31", "2023-09-30"]
injection_rate = 100  # 100 units/day injected
withdrawal_rate = 100  # 100 units/day withdrawn
max_volume = 500  # Maximum storage capacity
storage_costs = 2  # 2 units of currency per unit of gas per day

contract_value = price_gas_contract(injection_dates, withdrawal_dates, injection_rate, withdrawal_rate, max_volume, storage_costs)
print(f"The value of the gas contract is: {contract_value}")
