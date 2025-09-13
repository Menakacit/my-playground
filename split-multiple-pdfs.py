import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf, output_dir):
    """
    Split a single PDF into separate PDFs for each page.
    
    Args:
        input_pdf (str): Path to the input PDF file
        output_dir (str): Directory to store output PDF files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    
    # Create a subfolder for this PDF's pages
    pdf_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    # Read the input PDF
    try:
        pdf_reader = PdfReader(input_pdf)
        
        # Split each page
        for page_num in range(len(pdf_reader.pages)):
            # Create a new PDF writer
            pdf_writer = PdfWriter()
            
            # Add the current page to the writer
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Define output filename
            output_filename = os.path.join(pdf_output_dir, f"{base_name}_page_{page_num + 1}.pdf")
            
            # Write the page to a new PDF
            with open(output_filename, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"Created: {output_filename}")
    except Exception as e:
        print(f"Error processing {input_pdf}: {str(e)}")

def process_pdfs_in_folder(input_dir, output_dir):
    """
    Process all PDF files in the input directory and split them into single-page PDFs.
    
    Args:
        input_dir (str): Directory containing input PDF files
        output_dir (str): Directory to store all output PDFs
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all PDF files from input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"Processing: {pdf_path}")
        split_pdf(pdf_path, output_dir)

def main():
    # Input and output directories
    input_directory = "C:/Users/Public/Split PDF/input"
    output_directory = "C:/Users/Public/Split PDF/output"
    
    # Create input directory if it doesn't exist
    os.makedirs(input_directory, exist_ok=True)
    
    # Process all PDFs in the input directory
    process_pdfs_in_folder(input_directory, output_directory)

if __name__ == "__main__":
    main()