from rest_framework.response import Response
from rest_framework import status
import os
from PyPDF2 import PdfReader,PdfWriter


class MergeAndSplit:

    def split_pdf(self, uploaded_file, page_range):
        try:
            input_pdf=PdfReader(uploaded_file)
        except Exception as e:
            return Response({'error':'failed to read PDF:{}'.format(str(e))},status=status.HTTP_400_BAD_REQUEST)

        if page_range is not None:
            page_lists = list(map(int, page_range.split(',')))
        else:
            return Response({'error': 'Page range is not given'}, status=status.HTTP_400_BAD_REQUEST)

        # input_pdf = PdfReader(uploaded_file)

        if not os.path.exists('media/split_pdfs'):
            os.makedirs('media/split_pdfs')
        

        split_files = []
        for page_num in page_lists:
            if 1 <= page_num <= len(input_pdf.pages):
                output_pdf = PdfWriter()
                output_pdf.add_page(input_pdf.pages[page_num - 1])
                output_file_path = os.path.join('media', 'split_pdfs', f'split_page_{page_num}.pdf')
                with open(output_file_path, 'wb') as output_pdf_file:
                    output_pdf.write(output_pdf_file)
                split_files.append(output_file_path)

        return split_files

    def merge_pdfs(self, split_files):
        output_pdf = PdfWriter()

        for uploaded_file in split_files:
            input_pdf = PdfReader(uploaded_file)
            for page in range(len(input_pdf.pages)):
                output_pdf.add_page(input_pdf.pages[page])

        if not os.path.exists('media/merged_pdfs'):
            os.makedirs('media/merged_pdfs')

        output_file_path = os.path.join('media', 'merged_pdfs', 'merged_file.pdf')
        with open(output_file_path, 'wb') as output_pdf_file:
            output_pdf.write(output_pdf_file)

        return output_file_path