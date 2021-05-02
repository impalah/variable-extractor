"""
    Connects with database and stores medical report number and anonymized patiend_id

    TODO: logging

"""

import json
import sys
import getopt
import os
import io
import re

import uuid

class MedicalReportDb(object):


    def __init__(self, db_config: dict):
        """
            Initialize db

            If we are using models (django, SQLAlchemy), this does not apply

        """

        self.__db_config: dict = db_config

        self.__init_database(self.__db_config)


    def __init_database(self, db_config: dict) -> None:
        """
            Initialize database
            Mocked, not used

            :param db_config Database configuration
            :type str

            :raises: :class:`XXXError`: on any error

        """
        ...


    def store_patiend_id(self, mr_number: str, patient_id: str) -> None:
        """
            Store a record with the relationship between mr_number and patient_id

            :param mr_number Medical report number
            :type str

            :param patient_id Anonymized unique id for the medical record number
            :type str

            :raises: :class:`ValueError`: on every error (simplified for this exercise)

        """

        # Buld the record information in "database format"
        record = {
            'id': mr_number,
            'patiend_id': patient_id
        }

        self.__upsert_record('medical_record', 'id', record, overwrite=False)

    def __upsert_record(self, table_name: str, id_field: str, record_data: dict, overwrite: bool=False) -> None:
        """
            Store a record in the given table.

            :param table_name Table where to insert the record
            :type str

            :param id_field Table where to insert the record
            :type str

            :param record_data data to insert
            :type str

            :param overwrite If True, overwrite record if exists, if False, ignore insert
            :type bool

            :raises: :class:`ValueError`: on every error (simpliefied for this exercise)

        """

        # This will contain some database logic as:
        # - check_if_record_exists
        # - insert_record
        # - update_record
        ...       
