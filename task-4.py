# Author: Akshay Kollur
# Task Four for JPMorgan Chase & Co. Quantitative Research Virtual Work Experience: Investigate and Analyze Price Data: Bucket Fico Scores

# Some imports to be used throughout program
import pandas as pd
import numpy as np

# Function to compute Mean Squared Error (MSE)
def calculate_mse(fico_scores, mean):
    return np.mean((fico_scores - mean) ** 2)

# Function to quantize FICO scores into buckets and compute the MSE for each of the bucket
def quantize_fico_scores(fico_scores, num_buckets, lower_bound, upper_bound):
    # Filter FICO scores within the given range
    filtered_scores = [score for score in fico_scores if lower_bound <= score <= upper_bound]
    
    # Sort the FICO scores
    filtered_scores = sorted(filtered_scores)
    
    # Compute the step size for dividing the FICO scores into buckets
    bucket_size = len(filtered_scores) // num_buckets
    
    # Initialize the boundaries and bucket means
    bucket_boundaries = []
    bucket_means = []
    mse_values = []
    
    # Loop through and assign FICO scores to each bucket
    for i in range(num_buckets):
        # Define the start and end index of the bucket
        start_index = i * bucket_size
        # Ensure we capture all scores in the last bucket
        end_index = (i + 1) * bucket_size if i < num_buckets - 1 else len(filtered_scores)
        
        bucket_scores = filtered_scores[start_index:end_index]
        
        # Compute the mean of the current bucket
        bucket_mean = np.mean(bucket_scores)
        
        # Append the bucket's mean and boundary
        bucket_means.append(bucket_mean)
        bucket_boundaries.append((bucket_scores[0], bucket_scores[-1]))
        
        # Calculate MSE for the current bucket
        mse = calculate_mse(np.array(bucket_scores), bucket_mean)
        mse_values.append(mse)
    
    return bucket_boundaries, bucket_means, mse_values

# Reads the whole loan data file and sets it to a data variable
data = pd.read_csv("Task 3 and 4_Loan_Data.csv")

# Extracts only the FICO scores
fico_scores = data['fico_score'].values

# Chop up the FICO scores into 5 buckets preferably for each range
# 5 buckets for FICO scores 0-600 and 5 buckets for FICO scores 600-850
buckets = 5


# Set the ranges for the two chunks of buckets, [0-600] and [600-850] FICO scores
lower_bound_chunk_1 = 0
upper_bound_chunk_1 = 600
lower_bound_chunk_2 = 600
upper_bound_chunk_2 = 850

# Quantize the two chunks of the buckets
bucket_bounds_chunk_1, bucket_means_chunk_1, mse_values_chunk_1 = quantize_fico_scores(fico_scores, buckets, lower_bound_chunk_1, upper_bound_chunk_1)
bucket_bounds_chunk_2, bucket_means_chunk_2, mse_values_chunk_2 = quantize_fico_scores(fico_scores, buckets, lower_bound_chunk_2, upper_bound_chunk_2)

# Combine results from the two chunks of buckets
combined_bounds = bucket_bounds_chunk_1 + bucket_bounds_chunk_2
combined_means = bucket_means_chunk_1 + bucket_means_chunk_2
combined_mse_values = mse_values_chunk_1 + mse_values_chunk_2

# Print out the results to console
print(f"FICO Scores: {fico_scores}")
print(f"\nNumber of Buckets: 10 (5 for each chunk)")
print(f"\nBucket Boundaries and Means:")

for i in range(len(combined_bounds)):
    print(f"Bucket {i+1} (Range: {combined_bounds[i][0]} - {combined_bounds[i][1]}): Mean = {combined_means[i]}, MSE = {combined_mse_values[i]}")
    


