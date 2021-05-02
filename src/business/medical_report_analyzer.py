"""
    Analyzes medical reports and extracts Id and free section. Anonymizes patiend id

    TODO: logging

"""

import json
import sys
import getopt
import os
import io
import re
import hashlib


class MedicalReportAnalyzer(object):
    """
        Medical report analyzer
        TODO: Generalize to allow to configure a regex pattern instead of a fixed one
    """


    def __init__(self):
        """
            Initialization

        """
        ...

    def process(self, report_data:str) -> dict:
        """
            Process the text file and return dict with mr_number anonymized Id and free text

            :returns: Dictionary with the report data + the anonymized Id
            :rtype: dict

            :raises: :class:`ValueError`: If no report_data

        """

        if report_data:

            # 1. Search header and store MR number
            mr_number = self.__search_mr_number(report_data).strip()

            # 2. Anonymize MR number and generate patient_id
            patient_id = self.__anonymize_mr_number(mr_number)

            # 3. Search DIAGNOSES:
            free_text = self.__search_free_text(report_data)

            result = {
                'mr_number': mr_number,
                'patient_id': patient_id,
                'document_text': free_text                
            }

            return result

        else:

            # For simplicity throw a ValueError exception
            # In real environments we should use "custom" exceptions
            raise ValueError('No report data')


    def __search_mr_number(self, report_data: str) -> str:
        """
            Search mr_number

            :returns: Medical record number
            :rtype: str

            :raises: :class:`ValueError`: if not found

        """

        # Search for the string "MR:" followed by 0 or more spaces and a number
        match = re.search(r'(?<=Paciente:)(.*?)(?=Episodio:)', report_data)

        if match:
            # Get the last group of the regular expresion where the number is
            return match.group(1)
        else:
            # Raise not found exception
            # For simplicity we will rais a LookupError (python builtin)
            raise LookupError('No MR in report')

    def __search_free_text(self, report_data: str) -> str:
        """
            Search free text

            :returns: Free text with header
            :rtype: str

            :raises: :class:`ValueError`: if not found

        """

        compile_params = ["Motivo de consulta:(.*?)(?=$)"]
        compile_params.append(re.DOTALL)

        compiled_pattern = re.compile(*compile_params)

        search_params = [
            compiled_pattern,
            report_data,
        ]
        
        # Search for the string "MR:" followed by 0 or more spaces and a number
        match = re.search(*search_params)

        if match:
            # Get the last group of the regular expresion where the number is
            return match.group()
        else:
            # Raise not found exception
            # For simplicity we will raise a LookupError (python builtin)
            raise LookupError('No DIAGNOSE in report')


    def __anonymize_mr_number(self, mr_number: str) -> str:
        """
            Anonymize MR number by creating a hash

            :returns: anonymized mr number
            :rtype: str

        """

        h = hashlib.new('sha256')
        h.update(mr_number.encode('utf-8'))
        return str(int.from_bytes(h.digest(), byteorder="big") & (2 ** 64 - 1))

