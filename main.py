import PyPDF2

def read_pdf(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)  # Correct usage of PdfReader
        # Access the number of pages in the PDF
        number_of_pages = len(reader.pages)
        text = ''
        for page in range(number_of_pages):
            # Read each page
            text += reader.pages[page].extract_text()  # Extract text from each page
    return text  # Correct indentation for return statement