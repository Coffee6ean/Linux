import os
from pypdf import PdfReader
import re
import json 
from datetime import datetime   

# --- Functions --- #
def print_result(value):
    print('\n//----------------- Content Below -----------------//')
    print()
    print(value)
    print()
    print('//-------------------------------------------------//')    


def read_uploaded_pdf(pdf_file_path, metadata):
    """
    Read and process a PDF file containing activity data.

    Args:
        pdf_file_path (str): The file path of the uploaded PDF.
        metadata (dict): The metadata extracted from the PDF.

    Returns:
        int: 0 if the file is processed successfully, -1 if an error occurs.
    """
    # Check if the file exists and is a PDF
    if os.path.exists(pdf_file_path) and pdf_file_path.endswith('.pdf'):
        try:
            # Create a PdfReader object
            reader = PdfReader(pdf_file_path)

            # Initialize an empty string to hold the content of the entire document
            full_content_str = ""

            # Iterate through all pages and extract text
            #for page in reader.pages:
            #    full_content_str += page.extract_text() + "\n"  # Append text from each page
            first_page = reader.pages[0]

            # Reformat the extracted text
            header, body = pdf_reformatting(first_page.extract_text())

            # Include metadata in the processing
            print("Extracted Metadata:", metadata)

            # Convert the parsed data to JSON
            jsonify_parsed_data(metadata, header, body)

            return 0  # Indicate successful processing
        except Exception as e:
            print(f"An error occurred while processing the PDF: {e}")
            return -1  # Indicate an error
    else:
        print("The specified file does not exist or is not a PDF.")
        return -1  # Indicate an error


def extract_pdf_metadata(pdf_file_path):
    """
    Extract metadata from a PDF file.

    Args:
        pdf_file_path (str): The file path of the PDF.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """
    # Extract the filename without the extension
    filename = os.path.splitext(os.path.basename(pdf_file_path))[0]

    # Split the filename by hyphen
    result = filename.split(" - ")

    # Extract the issue date from the filename
    date_str = result[-1]
    issue_date = convert_date_format(date_str) if date_str else ""

    metadata = {
        "document_id": result[0],  # Document ID (first part)
        "document_title": result[1] if len(result) > 1 else "",  # Title (second part, if available)
        "document_subtitle": " - ".join(result[2:-1]) if len(result) > 2 else "",  # Subtitle (middle parts, if available)
        "issue_date": issue_date,
        "created_at": datetime.now().isoformat()  # Convert datetime to ISO format string
    }

    return metadata


def pdf_reformatting(pdf_content):
    """
    Reformats the content of a PDF by extracting the header and body sections based on user-defined anchor tags.

    Args:
        pdf_content (str): The content of the PDF as a string.

    Returns:
        tuple: A tuple containing two lists:
            - The formatted header as a list of words.
            - The formatted body as a list of lines.
    """
    # Prompt the user for anchor tags to identify sections of the content
    initial_anchor = input("Please enter the initial anchor tag: ")
    final_anchor = input("Please enter the final anchor tag: ")

    # Remove content after the final anchor tag
    content_up_to_final_anchor = re.match(fr'[\S\s]+?(?= {final_anchor})', pdf_content)
    if content_up_to_final_anchor:
        # Extract content up to the final anchor tag
        extracted_content = content_up_to_final_anchor.group()
    else:
        print("Error. Invalid content.")
        return [], []  # Return empty lists if content is invalid

    # Extract the header section and remove the initial anchor tag
    header_match = re.match(fr'[\S\s]+?({initial_anchor})', extracted_content)
    if header_match:
        header_content = header_match.group()
    else:
        print("Error. Initial anchor tag not found.")
        return [], []  # Return empty lists if initial anchor tag is not found

    # Extract the body by removing the header section
    body_content = re.sub(fr'[\S\s]+?({initial_anchor})', '', extracted_content).strip()

    # Format the header and body for output
    formatted_header = re.sub('\n', ' ', header_content).split()  # Split by whitespace
    formatted_body = body_content.split('\n') if body_content else []  # Split body into lines

    # Print the formatted results (optional)
    #print_result(formatted_header)
    #print_result(formatted_body)

    return formatted_header, formatted_body


def parse_header_data(formatted_header):
    """
    Create a new array with values from formatted_header that meet a condition.

    Args:
        formatted_header (list): A list of strings representing the header columns.

    Returns:
        list: A new list containing the values from formatted_header that meet the condition.
    """
    # Define the standard required attributes for each activity
    stdrd_cpm_body = {
        "id": "",
        "name": "",
        "duration": "",
        "start": "",
        "finish": "",
        "total_float": ""
    }

    # Condition: Keep values with length greater than 1
    condition = lambda x: len(x) > 1

    # Create a new list with values meeting the condition
    trimmed_columns = [col_val.lower() for col_val in formatted_header if condition(col_val)]

    # Initialize col_col to store matching standard attributes
    structured_header = []

    # Check for presence of trimmed columns in standard attributes
    for present_val in trimmed_columns:
        for stdrd_val in stdrd_cpm_body.keys():
            if present_val in stdrd_val.lower():  # Check for substring match (case insensitive)
                if stdrd_val not in structured_header:  # Avoid duplicates
                    structured_header.append(stdrd_val)  # Append matching standard attribute
                break  # Exit inner loop once a match is found

        # Break the outer loop if all keys have been found
        if len(structured_header) == len(stdrd_cpm_body):
            break

    return structured_header


def parse_activity_data(raw_data):
    """
    Parse raw activity data into a structured list of activity dictionaries.

    Args:
        raw_data (list): A list of strings representing raw activity data.

    Returns:
        list: A structured list of activities, where each activity is a dictionary of its components.
    """
    structured_activities = []
    current_parent = None

    for line in raw_data:
        # Remove leading/trailing whitespace
        line = line.strip()

        # Check if the line is a parent activity
        parent_match = re.match(
            r'^(.*?)(\s+\1)\s+(\d+\.?\d*?\s*d)\s+(\d{1,2}-\w{3}-\d{2,4})?\s*([A-Z]?)?\s*(\d{1,2}-\w{3}-\d{2,4})?\s*(-?\d+\.?\d*?d?)?\s*(\w+)?$', 
            line
        )

        if parent_match:
            # Extract components for the parent activity
            activity_id = parent_match.group(1).strip()  # Activity ID
            activity_name = activity_id  # Parent name is the same as ID
            duration = parent_match.group(3).strip()        # Duration
            start_date = parent_match.group(4).strip() if parent_match.group(4) else ''  # Start date
            finish_date = parent_match.group(6).strip() if parent_match.group(6) else ''  # Finish date
            total_float = parent_match.group(7) or ''      # Total float

            # Create a structured parent activity
            parent_activity = {
                "id": activity_id,
                "name": activity_name,
                "duration": duration,
                "start": start_date,
                "finish": finish_date,
                "total_float": total_float,
                "activities": []  # Initialize an empty list for child activities
            }
            structured_activities.append(parent_activity)
            current_parent = parent_activity  # Update the current parent
        else:
            # Check if the line is a child activity
            child_match = re.match(
                r'^([A-Z0-9-]+)\s+(.*?)\s+(\d+\.?\d*?\s*d)\s+(\d{1,2}-\w{3}-\d{2,4})?\s*([A-Z\*]?)?\s*(\d{1,2}-\w{3}-\d{2,4})?\s*(-?\d+\.?\d*?d?)?\s*(\w+)?$', 
                line
            )
            if child_match and current_parent:
                # Extract components for the child activity
                child_id = child_match.group(1).strip()
                child_name = child_match.group(2).strip()  # Name can include spaces and special characters
                child_duration = child_match.group(3).strip()
                child_start = child_match.group(4).strip() if child_match.group(4) else ''  # Start date
                child_finish = child_match.group(6).strip() if child_match.group(6) else ''  # Finish date
                child_total_float = child_match.group(7) or ''

                # Create a structured child activity
                child_activity = {
                    "id": child_id,
                    "name": child_name,
                    "duration": child_duration,
                    "start": child_start,
                    "finish": child_finish,
                    "total_float": child_total_float,
                }

                # Add the child activity to the current parent's activities list
                current_parent["activities"].append(child_activity)
            else:
                # If the line doesn't match the expected format, add it as a fallback
                structured_activities.append({"raw": line})

    return structured_activities


def jsonify_parsed_data(metadata, header_data, activity_data):
    """
    Convert parsed header and activity data into a JSON file, including metadata.

    Args:
        metadata (dict): A dictionary containing the extracted metadata.
        header_data (list): A list of strings representing the header data.
        activity_data (list): A list of strings representing the activity data.

    Returns:
        None
    """
    # Parse the header data into a structured format
    parsed_header = parse_header_data(header_data)

    # Parse the activity data into a structured format
    parsed_activities = parse_activity_data(activity_data)

    # Create the JSON object with metadata and content
    json_data = {
        "project_metadata": metadata,
        "project_content": {
            "header": parsed_header,
            "body": parsed_activities
        }
    }

    # Convert the JSON object to a string with indentation
    json_output = json.dumps(json_data, indent=2)

    # Create the 'results' directory if it doesn't exist
    output_directory = 'results'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Write the JSON output to a file
    output_file = os.path.join(output_directory, 'cpm.json')
    with open(output_file, 'w') as file:
        file.write(json_output)

    print(f"JSON output written to: {output_file}")


def convert_date_format(date_str):
    """
    Converts the date string to ISO 8601 format.
    
    Args:
        date_str (str): The date string in the format 'YYYY-MM-DD'.

    Returns:
        str: The date string in ISO 8601 format.
    """
    try:
        if isinstance(date_str, str):
            formatted = re.sub('(^)[\D]+', '', date_str)
            date_obj = datetime.strptime(formatted, '%Y.%m.%d' or '%Y/%m/%d' or '%Y-%m-%d') # Try parsing the date string in different formats
            return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            print_result(f"Invalid date format: {date_str}")
            return ""
    except ValueError:
        print_result(f"Invalid date format: {date_str}")
        return ""

