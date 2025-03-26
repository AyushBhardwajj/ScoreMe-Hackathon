import pdfplumber
import pandas as pd
import re  # For regex operations to clean cid(xxx)

# Load the PDF
pdf_path = "test3.pdf"

# Extract text data with positions
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted_text = page.extract_text()
        
        if extracted_text:
            # Split text into lines
            lines = extracted_text.split("\n")
            for line in lines:
                # Remove 'cid(xxx)' patterns using regex
                cleaned_line = re.sub(r"cid\(\d+\)", "", line)  # This removes the 'cid' patterns
                
                # Split by multiple spaces (assuming column separation)
                columns = list(filter(None, cleaned_line.split("  ")))  # Removes empty elements
                data.append(columns)

# Convert extracted data to DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel("output.xlsx", index=False, header=False)

print("✅ Data extracted and saved to output.xlsx")
