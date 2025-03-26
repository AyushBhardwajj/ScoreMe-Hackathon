import pandas as pd
import re

# Load the extracted raw Excel file
input_file = "output.xlsx"  # Use the correct file name
output_file = "cleaned_transactions.xlsx"

# Read the data
df = pd.read_excel(input_file, header=None)

# Define regex patterns for transaction rows
date_pattern = r"\d{2}-[A-Za-z]{3}-\d{2,4}"  # Matches dates like "04-Apr-2022"
amount_pattern = r"[\d,]+\.\d{2}"  # Matches amounts like "25,000.00"
balance_pattern = r"\d{1,3}(?:,\d{3})*\.\d{2}Dr?"  # Matches balance values

# Initialize list to store cleaned transactions
transactions = []

# Iterate through rows and extract relevant information
for row in df[0]:
    match = re.findall(date_pattern, str(row))  # Check for a date in the row
    if match:
        date = match[0]  # Get the first matched date
        details = row.split(date)[-1].strip()  # Extract details after the date
        
        # Extract transaction type (Cash, UPI, NEFT, etc.)
        transaction_type = "Unknown"
        if "Cash" in details:
            transaction_type = "Cash Deposit"
        elif "IMPS" in details or "UPI" in details:
            transaction_type = "UPI Transfer"
        elif "NEFT" in details:
            transaction_type = "NEFT Transfer"
        elif "Interest" in details or "Int.Coll" in details:
            transaction_type = "Interest Charged"
        elif "Lien Reversal" in details:
            transaction_type = "Lien Reversal"
        
        # Extract debit, credit, and balance amounts
        amounts = re.findall(amount_pattern, details)
        if len(amounts) == 3:
            debit, credit, balance = amounts
        elif len(amounts) == 2:
            debit, credit, balance = amounts[0], "", amounts[1]  # Handle missing credits
        elif len(amounts) == 1:
            debit, credit, balance = "", "", amounts[0]  # Only balance is available
        else:
            debit, credit, balance = "", "", ""
        
        # Store structured data
        transactions.append([date, transaction_type, details, debit, credit, balance])

# Create a structured DataFrame
columns = ["Date", "Transaction Type", "Details", "Debit (₹)", "Credit (₹)", "Balance (₹)"]
df_cleaned = pd.DataFrame(transactions, columns=columns)

# Save cleaned data to a new Excel file
df_cleaned.to_excel(output_file, index=False)

print(f"✅ Structured data saved to {output_file}")