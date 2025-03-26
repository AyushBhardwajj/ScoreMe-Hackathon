import pdfplumber
import pandas as pd
import re  
pdf_path = "test3.pdf"


data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted_text = page.extract_text()
        
        if extracted_text:
            
            lines = extracted_text.split("\n")
            for line in lines:
                
                cleaned_line = re.sub(r"cid\(\d+\)", "", line)  
                
                
                columns = list(filter(None, cleaned_line.split("  ")))  
                data.append(columns)


df = pd.DataFrame(data)


df.to_excel("output.xlsx", index=False, header=False)

print("✅ Data extracted and saved to output.xlsx")
