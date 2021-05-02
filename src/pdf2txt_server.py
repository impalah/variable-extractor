"""
	Webservices for converting pdf to txt
    - POST a pdf file, return txt in the request.

    NO AUTHENTICATION!


"""

import time
import threading

import json
import sys
import getopt
import os

from flask import Flask, request, Response

from common.logmanager import LogManager
from pdfutils.pdfmanager import PdfManager

# Initialize logger: Global logger variable for all this module
logger = LogManager()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/pdf', methods=['POST'])
def pdf():
    if request.method == 'POST':

        # Get data received and not "known" by flask
        req_data = request.data

        try:

            manager = PdfManager()
            result = manager.process(req_data)
            return Response(result, status=200, content_type='text/plain')

        except ValueError as ve:
            logger.critical("No data: {0}".format(repr(ve)))
            return Response("No data", status=400)

        except Exception as e:
            logger.critical("Webservice general ERROR: {0}".format(repr(e)))
            return Response(status=500)

if __name__ == '__main__':
    # All these parameters should be in a config file or environment variables ...
    app.run(host="0.0.0.0", port=5000)
