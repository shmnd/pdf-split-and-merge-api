from rest_framework.response import Response
from rest_framework import status

from io import BytesIO
import os
from PyPDF2 import PdfReader,PdfWriter


class MergeAndSplit():
    def __init__(self, error_messages):
        self.error_message = error_messages

    def split_pdf(self, uploaded_file, page_range):
        try:
            input_pdf=PdfReader(uploaded_file)
        except Exception as e:
            self.error_message.append(f'failed to read PDF:{str(e)}')

        if page_range is not None:
            page_lists = list(map(int, page_range.split(',')))
        else:
            self.error_message.append(f'Page range is not given')

        split_files = []

        for page_num in page_lists:
            if 1 <= page_num <= len(input_pdf.pages):
                output_pdf = PdfWriter()
                output_pdf.add_page(input_pdf.pages[page_num - 1])

                '''Create a BytesIO object to hold the PDF data'''
                output_pdf_buffer=BytesIO()
                output_pdf.write(output_pdf_buffer)

                '''Reset the buffer position to the beginning'''
                output_pdf_buffer.seek(0)

                '''Append the BytesIO object to the list'''
                split_files.append(output_pdf_buffer)

        return split_files



    def merge_pdfs(self, split_files):
        output_pdf = PdfWriter()
        
        for uploaded_file in split_files:
            input_pdf = PdfReader(uploaded_file)

            for page in range(len(input_pdf.pages)):
                output_pdf.add_page(input_pdf.pages[page])

        output_file = os.path.join('media', 'merged_pdfs')
        os.makedirs(output_file, exist_ok=True)
        output_file_path=os.path.join('media', 'merged_pdfs','merged_file.pdf')

        with open(output_file_path, 'wb') as output_pdf_file:
            output_pdf.write(output_pdf_file)
            output_pdf_file.close()
        
        return output_file_path
    

