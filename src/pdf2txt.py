"""
	Command line utility for converting from pdf to text

    - Part of the basic business (decode parameters, open file and main function) are in fucntion, not classes.

"""

import time
import threading

import json
import sys
import getopt
import os
import signal

from common.logmanager import LogManager
from pdfutils.pdfmanager import PdfManager

# Initialize logger: Global logger variable for all this module
logger = LogManager()

def show_help():
    """
        Show command help
    """
    help_line = "pdf2txt.py <-i input_file | -o output_file> [-h] [-p]"
    logger.info(help_line)

def read_pdf_file(input_file):
    """
        Read the PDF file and return content as bytes

        :param: input_file: Name of the PDF file
        :type: str

        :returns: Content of the pdf file or None if error
        :rtype: bytes

    """

    if not os.path.isfile(input_file):
        logger.error("Input file does not exists.")
        return None

    with open(input_file, "rb") as f:
        pdf_binary = f.read()

    return pdf_binary


def main(argv):

    # Get parameters (it is here for simplicity, it should be in a function)
    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["input_file=", "output_file="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    input_file = None
    output_file = None

    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg

    if not input_file or not output_file:
        show_help()
        sys.exit()

    try:

        # Open and read the file
        logger.info('Input file: {0}'.format(input_file))

        pdf_binary = read_pdf_file(input_file)

        if pdf_binary:

            # logger.debug('Input file opened. Content: {0}'.format(pdf_binary))
            logger.debug('Input file opened')

            # Encode file
            pdf_helper = PdfManager()
            result = pdf_helper.process(pdf_binary)

            logger.debug('PDF file processed. Content: {0}'.format(result))
            # logger.debug('PDF file processed')

            # Save file
            with open(output_file, "w") as text_file:
                text_file.write(result)

            logger.debug('Text file saved: {0}'.format(output_file))

        else:

            logger.critical('Error reading input file')

    except Exception as e:

        # This is not neccesary as exceptions are controlled in caller function
        logger.critical(
            "Exception on pdf2txt service: {0}".format(repr(e)))


if __name__ == "__main__":

    try:
        logger.info("Starting PDF to text service")
        main(sys.argv[1:])
        logger.info("PDF to text service finished")

    except Exception as e:
        logger.critical(
            "*** Exception on PDF to text service: {0}".format(repr(e)))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

