# Author: Akshay Kollur
# Task Three for JPMorgan Chase & Co. Quantitative Research Virtual Work Experience: Credit Risk Analysis

# Some imports to be used throughout the program:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Preprocess Data
def preprocess_data(df):
    """
    Preprocess the data by handling missing values and scaling the features.
    """
    # Clean data: drop any rows with missing values (optional, depends on your data quality)
    df = df.dropna()

    # Define features and target
    features = ['credit_lines_outstanding', 'loan_amt_outstanding', 'total_debt_outstanding', 'income', 'years_employed', 'fico_score']
    target = 'default'

    # Extract the features and target
    x = df[features]
    y = df[target]

    # Standardize the features using StandardScaler
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    
    return x_scaled, y, scaler

# Train model
def train_model(x_train, y_train):
    """
    Train a logistic regression model to predict default.
    """
    model = LogisticRegression()
    model.fit(x_train, y_train)
    return model

# Calculate Expected Loss with this formula....
# The formula for expected loss is:
# Expected Loss=PD×Loan Amount×(1−Recovery Rate)
def calculate_expected_loss(model, scaler, loan_details, recovery_rate=0.10):
    """
    Calculate the expected loss based on the predicted probability of default (PD)
    """
    # Prepare loan_details as a dataframe and scale the features
    loan_data = pd.DataFrame([loan_details])
    loan_data_scaled = scaler.transform(loan_data)

    # Predict the probability of default (PD)
    probability_of_default = model.predict_proba(loan_data_scaled)[0][1]

    # Calculate expected loss
    loan_amt = loan_details['loan_amt_outstanding']
    expected_loss = probability_of_default * (loan_amt * (1 - recovery_rate))
    
    return expected_loss


# Load the data
# Load the dataset from the specified file path.
loanData = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# Preprocess the data
x, y, scaler = preprocess_data(loanData)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = train_model(x_train, y_train)

# Evaluate the model
y_pred = model.predict(x_test)
print("Model Accuracy: ", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Example of how to calculate the expected loss for a new loan
new_loan_details = {
    # Example number of credit lines the borrower has
    'credit_lines_outstanding': 5,
     # Example loan amount outstanding               
    'loan_amt_outstanding': 2000,
    # Example total debt outstanding             
    'total_debt_outstanding': 5000,
    # Example annual income of the borrower              
    'income': 30000,
    # Example years employed                             
    'years_employed': 3,
    # Example FICO credit score                        
    'fico_score': 600                            
}

# Using the example data for a new loan we can notice the accuracy 
expected_loss = calculate_expected_loss(model, scaler, new_loan_details)
print(f"Expected Loss for the new loan: ${expected_loss:.2f}")

