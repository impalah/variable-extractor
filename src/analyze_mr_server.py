"""
	Webservices for analyzing medical report

    NO AUTHENTICATION!


"""

import time
import threading

import json
import sys
import getopt
import os

from flask import Flask, request, Response, jsonify

from common.logmanager import LogManager
from business.medical_report_analyzer import MedicalReportAnalyzer
from business.medical_report_db import MedicalReportDb

# Initialize logger: Global logger variable for all this module
logger = LogManager()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/medical-report', methods=['POST'])
def medical_report():

    if request.method == 'POST':

        # Get data received and not "known" by flask
        req_data = request.data 

        logger.debug('Request data. Content: {0}'.format(req_data.decode('utf-8')))

        try:

            # Analyze report
            analyzer = MedicalReportAnalyzer()
            medical_record = analyzer.process(req_data.decode('utf-8'))

            logger.debug('Medical Record File processed. Content: {0}'.format(medical_record))
            # logger.debug('Medical Record File processed')

            # Store on database
            # db_config should be in environment variables (docker/kubernetes)
            db_manager = MedicalReportDb({'db_config': 'some_db_config'})

            db_manager.store_patiend_id(
                medical_record['mr_number'],
                medical_record['patient_id']
                )

            # Delete mr_number
            medical_record.pop('mr_number')

            return jsonify(medical_record)

        except ValueError as ve:
            logger.critical("No data: {0}".format(repr(ve)))
            return Response("No data", status=400)

        except Exception as e:
            logger.critical("Webservice general ERROR: {0}".format(repr(e)))
            return Response(status=500)

if __name__ == '__main__':
    # All these parameters should be in a config file or environment variables ...
    app.run(host="0.0.0.0", port=5001)
