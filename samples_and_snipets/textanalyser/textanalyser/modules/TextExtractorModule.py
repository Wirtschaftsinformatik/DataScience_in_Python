import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .ErrorExceptionModule import *


class File:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_text(self):
        # initialize
        resource_manager = PDFResourceManager()
        file_handle = io.StringIO()
        converter = TextConverter(resource_manager, file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        # open file and read by page
        try:
            with open(self.filepath, 'rb') as file:
                for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
                    page_interpreter.process_page(page)

                text = file_handle.getvalue()

            # close handlers
            converter.close()
            file_handle.close()

            # return text
            if text:
                return text
            else:
                raise NoTextFoundError

        # exception handling
        except FileNotFoundError:
            print('File ' + self.filepath + ' not found!')
        except NoTextFoundError:
            print('Text is Empty')

