#-------------------------------------------------------------------------------
# Name:        pdfReportGenerator
# Purpose:     Generate PDF report form Nineteen68 Reports JSON
#
# Author:      ranjan.agrawal
#
# Created:     30-11-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
from pdfkitlib_override import pdfkit
from generatepdf import GeneratePDFReport
from generatepdf_batch import GeneratePDFReportBatch

pdfkit_conf = None
wkhtmltopdf_path = os.environ["NINETEEN68_HOME"] + "/Scripts/wkhtmltox/bin/wkhtmltopdf.exe"
if os.path.exists(wkhtmltopdf_path):
    pdfkit_conf = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
else:
    raise ImportError('No module named wkhtmltopdf')
