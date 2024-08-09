# Activity Data Parser

## Purpose
The Activity Data Parser is a Python package designed to parse raw activity data from PDFs and convert it into a structured JSON format. It can handle various types of activity data, including parent and child activities, and extract relevant information such as IDs, names, durations, start dates, finish dates, total float values, and metadata.

## Functionality
The package provides the following functionality:

1. **Parsing Raw Activity Data**: The `parse_activity_data` function takes a list of raw activity data strings as input and returns a structured list of activity dictionaries.

2. **Identifying Parent and Child Activities**: The parsing logic differentiates between parent and child activities based on specific patterns in the input data.

3. **Extracting Activity Components**: The package extracts the following components from each activity:
   - ID
   - Name
   - Duration
   - Start Date
   - Finish Date
   - Total Float
   - Additional Information (if present)

4. **Including Metadata**: The package can extract metadata from the PDF, including:
   - Document ID
   - Document Title
   - Document Subtitle
   - Issue Date
   - Creation Timestamp

5. **Hierarchical Structure**: The parsed activities are organized in a hierarchical structure, with child activities being associated with their respective parent activities.

6. **JSON Conversion**: The `jsonify_parsed_data` function takes the parsed activity data and metadata, converting them into a structured JSON object, which can be saved to a file or used for further processing.

## Summary of Requirements

### Parent Activities:
- The ID will be repeated in the line.
- The ID can contain spaces and is a combination of upper and lower case characters.

### Child Activities:
- The ID is in uppercase letters, may contain numbers, and is connected by dashes.
- The name can include spaces and special characters.
- The duration is indicated by a number followed by 'd'.
- The start date is in the format DD-MMM-YY, which can include additional characters like 'A' or '*'.
- The finish date and total float may be present but are optional.

## Limitations
- The package relies on regex patterns to match and extract activity components. If the input data deviates significantly from the expected format, the parsing may not work as intended.
- In cases where both the start and finish dates are missing, the package assigns the first date value it encounters to the start date property. This means that if the finish date is missing, it will be treated as the start date, and the actual start date will be considered missing.
- The package assumes that the ID and name of a parent activity are the same or that the ID is contained within the name. If this assumption is not met, the parsing may not correctly identify parent activities.

## Usage
To use the Activity Data Parser, you can import the necessary functions and provide the raw activity data as input:

```python
from activity_data_parser import parse_activity_data, jsonify_parsed_data, read_uploaded_pdf, extract_pdf_metadata

# Prompt the user to enter the PDF file path
pdf_file_path = input("Please enter the path to the PDF file: ")

# Check if the file exists
if os.path.exists(pdf_file_path) and pdf_file_path.endswith('.pdf'):
    # Extract metadata from the PDF
    metadata = extract_pdf_metadata(pdf_file_path)
    
    # Process the PDF file and include the metadata
    if read_uploaded_pdf(pdf_file_path, metadata) == 0:
        print("PDF processing completed successfully.")
    else:
        print("An error occurred during PDF processing.")
else:
    print("The specified file does not exist or is not a PDF.")
```

## Metadata Structure
When processing the PDF, the metadata is structured as follows:

```python
metadata = {
    "document_id": result,  # Document ID (first part)
    "document_title": result if len(result) > 1 else "",  # Title (second part, if available)
    "document_subtitle": result if len(result) > 2 else "",  # Subtitle (third part, if available)
    "issue_date": convert_date_format(result) if len(result) > 3 else "",  # Date (fourth part, if available)
    "created_at": datetime.now()  # Current timestamp
}
```
# Conclusion

The Activity Data Parser is a useful tool for converting raw activity data from PDFs into a structured format, making it easier to work with and analyze. However, it's important to be aware of its limitations and ensure that the input data matches the expected format to achieve accurate parsing results.

If you encounter any issues or have further requirements, please let me know, and I'll be happy to assist you in refining the parsing logic or expanding the functionality of the package.
