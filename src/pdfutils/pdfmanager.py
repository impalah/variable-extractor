"""
    Wrapper for pdftotext for converting a PDF file to text
    Logging pending :-(

    * Future improvement: use composition to allow different PDF to text libraries

"""

import json
import sys
import getopt
import os
import io

import uuid

import pdftotext

class PdfManager(object):


    def __init__(self):
        """
            Initialize stuff if needed

        """
        ...


    def process(self, binary_data: bytes) -> str:
        """
            Process the PDF file and return the result

            :returns: Text representation of pdf file
            :rtype: str

            :raises: :class:`ValueError`: If no binary_data

        """

        if binary_data:

            return self._process_pdf_file(binary_data)

        else:

            # For simplicity throw a ValueError exception
            # In real environments we should use "custom" exceptions
            raise ValueError('No PDF data')


    def _process_pdf_file(self, binary_data: bytes) -> str:
        """
            This function will be mocked in tests as it uses pdftotext library
            pdftotext is a wrapper over libpoppler C library

            :param binary_data Binary representation of a PDF file
            :type bytes

            :returns: Text representation of pdf file
            :rtype: str

        """

        # Create a stream and send to pdftotext
        f = io.BytesIO(binary_data)
        pdf = pdftotext.PDF(f)

        # Return the full text
        return "\n\n".join(pdf)


