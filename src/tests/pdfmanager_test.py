import unittest
from unittest.mock import patch

from pdfutils.pdfmanager import PdfManager


class PdfManagerTest(unittest.TestCase):
    """
        Just test PdfManager
    """

    # SetUp not needed as is a very simple testing
    # def setUp(self):
    #     self.manager = PdfManager()

    def test_ok(self):

        # Mock the call to pdftotext
        with patch.object(PdfManager, '_process_pdf_file', return_value='XXXX') as mock_method:

            manager = PdfManager()
            result = manager.process('fake pdf data')

        self.assertEqual(result, 'XXXX')

    def test_no_data(self):
        
        manager = PdfManager()

        with self.assertRaises(ValueError) as context:
            manager.process(None)

        self.assertTrue('No PDF data' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
