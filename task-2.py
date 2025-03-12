# Author: Akshay Kollur
# Task Two for JPMorgan Chase & Co. Quantitative Research Virtual Work Experience: Price a Storage Commodity Contract

# Various imports to be used throughout Task Two
import csv
from datetime import datetime



# Helper function to parse the CSV data
def read_gas_data(file_path):
    """
    Reads gas price data from a CSV file and returns a list of price data.

    Inputs:
    - file_path (str): The path to the CSV file.

    Outputs:
    - price_data (list): A list of dictionaries containing 'Date' and 'Price' for each record.
    """
    price_data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['Date'] = datetime.strptime(row['Dates'], '%m/%d/%y')  # Parse the date
            row['Price'] = float(row['Prices'])  # Convert the price to a float
            price_data.append(row)
    return price_data

# Function to calculate the cost of gas injected
def calculate_injection_cost(inject_volume, inject_price):
    """
    Calculates the cost of injecting gas into storage.
    
    Inputs:
    - inject_volume (float): The volume of gas being injected (in MMBtu).
    - inject_price (float): The price of gas on the injection date (in $/MMBtu).
    
    Outputs:
    - float: The total cost of injection.
    """
    return inject_volume * inject_price

# Function to calculate the revenue from gas withdrawal
def calculate_withdrawal_revenue(withdraw_volume, withdraw_price):
    """
    Calculates the revenue from withdrawing gas from storage.
    
    Inputs:
    - withdraw_volume (float): The volume of gas being withdrawn (in MMBtu).
    - withdraw_price (float): The price of gas on the withdrawal date (in $/MMBtu).
    
    Outputs:
    - float: The total revenue from withdrawal.
    """
    return withdraw_volume * withdraw_price

# Function to calculate storage cost (constant storage cost for simplicity)
def calculate_storage_cost(current_storage, storage_cost_per_unit):
    """
    Calculates the cost of storing gas in storage.
    
    Inputs:
    - current_storage (float): The amount of gas currently stored (in MMBtu).
    - storage_cost_per_unit (float): The cost to store one unit of gas per day (in $/MMBtu/day).
    
    Outputs:
    - float: The total storage cost.
    """
    return current_storage * storage_cost_per_unit

# Function to calculate the total storage volume after injection
def calculate_injected_volume(current_storage, inject_volume, max_volume):
    """
    Calculates the new storage volume after injecting gas.
    
    Inputs:
    - current_storage (float): The current volume of gas in storage (in MMBtu).
    - inject_volume (float): The volume of gas to inject (in MMBtu).
    - max_volume (float): The maximum capacity of the storage (in MMBtu).
    
    Outputs:
    - float: The new total storage volume after injection.
    """
    inject_volume = min(inject_volume, max_volume - current_storage)
    return current_storage + inject_volume

# Function to calculate the total storage volume after withdrawal
def calculate_withdrawn_volume(current_storage, withdraw_volume):
    """
    Calculates the new storage volume after withdrawing gas.
    
    Inputs:
    - current_storage (float): The current volume of gas in storage (in MMBtu).
    - withdraw_volume (float): The volume of gas to withdraw (in MMBtu).
    
    Outputs:
    - float: The new total storage volume after withdrawal.
    """
    return max(0, current_storage - withdraw_volume)

# Function to calculate the contract value
def price_gas_contract(file_path, injection_dates, withdrawal_dates, injection_rate, withdrawal_rate, max_volume, storage_costs):
    """
    Calculates the value of a gas storage contract based on provided parameters.

    Inputs:
    - file_path (str): Path to the Nat_Gas CSV file
    - injection_dates (list): Dates for gas injection.
    - withdrawal_dates (list): Dates for gas withdrawal.
    
    - prices (dict): Dictionary mapping dates to gas prices.
    
    - injection_rate (float): Maximum rate at which gas can be injected.
    - withdrawal_rate (float): Maximum rate at which gas can be withdrawn.
    - max_volume (float): Maximum storage capacity.
    - storage_costs (float): Cost of storing gas per unit volume per time step.

    Outputs:
    - float: Value of the contract.
    """
    # Read price data from the CSV file
    price_data = read_gas_data(file_path)
    
    # Create a dictionary for fast lookup of price by date
    price_lookup = {row['Date']: row['Price'] for row in price_data}
    
    # Initialize variables for tracking gas volume and financial
    current_storage = 0
    total_cost = 0
    total_revenue = 0
    
    # Process each injection event
    for inject_date_str in injection_dates:
        inject_date = datetime.strptime(inject_date_str, '%Y-%m-%d')
        inject_price = price_lookup.get(inject_date)  # Get the price for the injection date
        if inject_price is None:
            raise ValueError(f"No price data available for injection date {inject_date_str}")
        
        inject_volume = injection_rate  # Assuming full injection for each day
        # Calculate new storage volume after injection
        current_storage = calculate_injected_volume(current_storage, inject_volume, max_volume)
        # Add the injection cost to the total cost
        total_cost += calculate_injection_cost(inject_volume, inject_price)

    # Process each withdrawal event
    for withdraw_date_str in withdrawal_dates:
        withdraw_date = datetime.strptime(withdraw_date_str, '%Y-%m-%d')
        withdraw_price = price_lookup.get(withdraw_date)  # Get the price for the withdrawal date
        if withdraw_price is None:
            raise ValueError(f"No price data available for withdrawal date {withdraw_date_str}")
        
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

contract_value = price_gas_contract("Nat_Gas.csv", injection_dates, withdrawal_dates, injection_rate, withdrawal_rate, max_volume, storage_costs)
print(f"The value of the gas contract is: {contract_value}")

    
    
    
    
    
    
    
    
    
    
    
    
    
    