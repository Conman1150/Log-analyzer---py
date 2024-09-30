import pandas as pd
import re

# Function to read the log file
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

# Function to extract failed login attempts (or specific events)
def extract_failed_logins(logs):
    failed_attempts = []
    for line in logs:
        # Debug: Print each line
        print(f"Processing line: {line.strip()}")

        # Check for specific event IDs or keywords related to login failures
        if 'Event ID: 5379' in line or 'failed login' in line.lower() or 'logon failure' in line.lower():
            # Use regex to extract timestamp (format: 'Sun Sep 29 23:52:58 2024')
            match = re.search(r'(\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4})', line)
            if match:
                timestamp = match.group(0)
                failed_attempts.append({'timestamp': timestamp, 'log_entry': line.strip()})
                print(f"Match found: {line.strip()}")
    
    return pd.DataFrame(failed_attempts)

# Function to save the extracted data to a CSV file
def save_to_csv(dataframe, output_file):
    dataframe.to_csv(output_file, index=False)

# Main function
if __name__ == "__main__":
    # Path to your log file
    log_file_path = 'extracted_security_logs.txt'

    # Read and parse the log file
    logs = read_log_file(log_file_path)

    # Extract failed login attempts
    failed_logins_df = extract_failed_logins(logs)

    # Save the results to a CSV file
    output_csv = 'failed_logins_report.csv'
    save_to_csv(failed_logins_df, output_csv)

    print(f"Analysis complete. Extracted data saved to {output_csv}")
