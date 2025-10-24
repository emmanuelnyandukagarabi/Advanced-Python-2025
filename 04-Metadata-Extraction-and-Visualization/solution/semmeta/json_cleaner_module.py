# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import JSON module for reading and writing metadata files
import json

# Import regular expressions module for parsing numeric values and units
import re


# Class for cleaning and formatting SEM metadata from JSON files
class JsonCleaner:
    def __init__(self, cleaned_data={}):                       
        # Initialize the cleaned_data dictionary to store processed metadata
        self.cleaned_data = cleaned_data


    def load_json(self, jsfile):
        # Open the JSON file and load its contents into a Python dictionary
        with open(jsfile, 'r') as f:
            return json.load(f)


    def clean_value(self, value):
        """
        Extracts numeric value and unit from strings, e.g., 'AP_WD =  3.18 mm'
        """
        
        # Use regex to extract a numeric value and its unit from the string
        match = re.search(r'([\d.]+)\s*([a-zA-Zμ]+)', value)
        
        # If a match is found, return the formatted value and unit
        if match:
            return match.group(1) + ' ' + match.group(2)
        
        # If no match is found, return the original value unchanged
        return value


    def clean_dict(self, data):
        """
        Cleans a metadata dictionary by parsing string values
        and skipping any entries with None values.
        """
        
        # Initialize an empty dictionary to store cleaned entries
        cleaned = {}
        
        # Iterate over each key-value pair in the input dictionary
        for key, value in data.items():
            
            # Skip entries with None values
            if value is None:
                continue
            
            # If the value is a string, clean it using regex
            if isinstance(value, str):
                cleaned[key] = self.clean_value(value)
            
            # Otherwise, keep the value as-is
            else:
                cleaned[key] = value
        
        # Return the cleaned dictionary
        return cleaned


    def process(self, jsfile):
        # Load raw metadata from the JSON file
        raw_data = self.load_json(jsfile)
        
        # Clean the raw metadata and store the result
        self.cleaned_data = self.clean_dict(raw_data)
        
        # Return the cleaned metadata dictionary
        return self.cleaned_data


    def save_cleaned(self, output_path):
        # Save the cleaned metadata to a new JSON file with indentation
        with open(output_path, 'w') as f:        
            # Write cleaned metadata to JSON file with readable formatting (2-space indentation)
            json.dump(self.cleaned_data, f, indent=2)
