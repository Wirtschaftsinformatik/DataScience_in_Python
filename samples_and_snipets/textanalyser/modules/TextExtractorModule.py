import io
import pdfminer

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import resolve1

from .ErrorExceptionModule import *


class File:

    @staticmethod
    def extract_text(filepath, progress_bar):
        # initialize
        laparams = pdfminer.layout.LAParams()
        setattr(laparams, 'all_texts', True)
        resource_manager = PDFResourceManager()
        file_handle = io.StringIO()
        converter = TextConverter(resource_manager, file_handle, laparams=laparams)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        # open file and read by page
        try:
            with open(filepath, 'rb') as file:

                # getting pdf meta data
                parser = PDFParser(file)
                doc = PDFDocument(parser)
                print(doc.info)

                # ui stuff for progess bar
                count = 1
                progress_bar.setMaximum(resolve1(doc.catalog['Pages'])['Count'])

                for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
                    progress_bar.setValue(count)
                    page_interpreter.process_page(page)
                    count += 1

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
            print('File ' + filepath + ' not found!')
        except NoTextFoundError:
            print('Text is Empty')

