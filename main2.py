import pandas as pd
import re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('FIR_Details_Data.csv')

# Regular expression pattern to match numbers followed by KM
pattern_km = re.compile(r'(\d+)\s+KM')

# Regular expression pattern to match numbers followed by MTRS
pattern_mtrs = re.compile(r'(\d+)\s+MTRS')

def replace_patterns(text):
    if isinstance(text, str):
        # If KM is present
        match_km = re.search(pattern_km, text)
        if match_km:
            return match_km.group(1)
        
        # If MTRS is present
        match_mtrs = re.search(pattern_mtrs, text)
        if match_mtrs:
            return str(int(match_mtrs.group(1)) / 1000)
        
        # If neither KM nor MTRS is present and text can be converted to an integer
        try:
            return str(int(text) / 1000)
        except ValueError:
            return text  # Return the original string if it cannot be converted to an integer
    
    return text  # Return the original value if it's not a string



# Apply replacements to the specified column
df['Distance from PS'] = df['Distance from PS'].apply(replace_patterns)

# Save the modified DataFrame back to a CSV file
df.to_csv('modified_file.csv', index=False)
