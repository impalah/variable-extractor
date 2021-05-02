"""
	Command line utility for analyzing medical report
   - Extract medical record number and free text.
   - Anonymize MR number.
   - Stores anonymized MR number in database

"""

import time
import threading

import json
import sys
import getopt
import os
import signal

from common.logmanager import LogManager
from business.medical_report_analyzer import MedicalReportAnalyzer
from business.medical_report_db import MedicalReportDb

# Initialize logger: Global logger variable for all this module
logger = LogManager()

def show_help():
    """
        Show command help
    """
    help_line = "analyze_mr.py <-i input_file> [-h]"
    logger.info(help_line)

def read_text_file(input_file):
    """
        Read the text file and return content as string

        :param: input_file: Name of the text file
        :type: str

        :returns: Content of the text file or None if error
        :rtype: str

    """

    if not os.path.isfile(input_file):
        logger.error("Input file does not exists.")
        return None

    with open(input_file, "r") as f:
        text_content = f.read()

    return text_content


def main(argv):

    # Get parameters (it is here for simplicity, it should be in a function)
    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["input_file=", "output_file="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    input_file = None

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

        record_text = read_text_file(input_file)

        if record_text:

            logger.debug('Input file opened')

            # Analyze report
            analyzer = MedicalReportAnalyzer()
            medical_record = analyzer.process(record_text)

            logger.debug('Medical Record File processed. Content: {0}'.format(medical_record))
            # logger.debug('Medical Record File processed')

            # Store on database
            # db_config should be in environment variables (docker/kubernetes)
            db_manager = MedicalReportDb({'db_config': 'some_db_config'})

            db_manager.store_patiend_id(
                medical_record['mr_number'],
                medical_record['patient_id']
                )

            logger.debug('Medical Record Number stored.')

            # Delete the field mr_number
            medical_record.pop('mr_number')

            # Save json file
            with open(output_file, "w") as text_file:
                text_file.write(json.dumps(medical_record))

            logger.debug('Text file saved: {0}'.format(output_file))
            
        else:

            logger.critical('Error reading input file')

    except Exception as e:

        # This is not neccesary as exceptions are controlled in caller function
        logger.critical(
            "Exception on analyze_mr service: {0}".format(repr(e)))


if __name__ == "__main__":

    try:
        logger.info("Starting MR Analyzer service")
        main(sys.argv[1:])
        logger.info("MR Analyzer service finished")

    except Exception as e:
        logger.critical(
            "*** Exception on MR Analyzer service: {0}".format(repr(e)))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

