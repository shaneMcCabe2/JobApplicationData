import pandas as pd
from datetime import datetime
import pytz
import os
import sqlite3

# Function to get user input and add it to the DataFrame
def add_job_details(df):
    company = input("Enter the company name: ")
    job_title = input("Enter the job title: ")
    job_url = input("Enter the job URL: ")
    pay = input("Enter the pay: ")
    
    # Get current datetime in EST
    est_timezone = pytz.timezone('US/Eastern')
    current_datetime = datetime.now(est_timezone)
    
    return pd.DataFrame({
        'Company': [company],
        'Job Title': [job_title],
        'Job URL': [job_url],
        'Pay': [pay],
        'Datetime': [current_datetime]
    })

# Check if the DataFrame file exists
file_path = 'job_details.csv'
if os.path.isfile(file_path):
    # If the file exists, load the existing DataFrame
    df = pd.read_csv(file_path)
    print("Loaded existing DataFrame:")
else:
    # If the file doesn't exist, create a new empty DataFrame
    columns = ['Company', 'Job Title', 'Job URL', 'Pay', 'Datetime']
    df = pd.DataFrame(columns=columns)
    print("Created new DataFrame.")

# Initialize the SQLite database
db_path = 'job_details.db'
conn = sqlite3.connect(db_path)

# Create the table if it doesn't exist
create_table_query = '''
    CREATE TABLE IF NOT EXISTS job_details (
        "Company" TEXT,
        "Job Title" TEXT,
        "Job URL" TEXT,
        "Pay" TEXT,
        "Datetime" TEXT
    )
'''
conn.execute(create_table_query)

# Prompt the user to add job details
while True:
    new_row = add_job_details(df)
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Insert the new row into the database
    new_row.to_sql('job_details', conn, if_exists='append', index=False)
    
    # Ask the user if they want to add more job details
    add_more = input("Do you want to add more job details? (y/n): ")
    if add_more.lower() != 'y':
        break

# Save the updated DataFrame to the CSV file
df.to_csv(file_path, index=False)

print("\nFinal DataFrame:")
print(df)

print("\nDatabase updated successfully.")

# Close the database connection
conn.close()