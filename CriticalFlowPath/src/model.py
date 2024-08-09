import os
from pypdf import PdfReader
from lib.pdf_to_jason import read_uploaded_pdf, extract_pdf_metadata

def process_pdf_file():
    """
    Prompt the user for a PDF file path, extract metadata, and read the PDF file.
    """
    # Prompt the user to enter the PDF file path
    pdf_file_path = input("Please enter the path to the PDF file: ")

    # Check if the file exists
    if os.path.exists(pdf_file_path) and pdf_file_path.endswith('.pdf'):
        # Extract metadata from the PDF
        metadata = extract_pdf_metadata(pdf_file_path)

        # Process the PDF file and include the metadata and anchors
        if read_uploaded_pdf(pdf_file_path, metadata) == 0:
            print("PDF processing completed successfully.")
        else:
            print("An error occurred during PDF processing.")
    else:
        print("The specified file does not exist or is not a PDF.")


# Call the function to process the PDF file
process_pdf_file()
