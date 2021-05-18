#-------------------------------------------------------------------------------
# Name:        pdfkitlib_override
# Purpose:     Override pdfkit library's internal methods to deal with
#              application specific issues
#
# Author:      ranjan.agrawal
#
# Created:     14-12-2018
# Copyright:   (c) ranjan.agrawal 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import subprocess, sys, codecs, pdfkit

__all__ = ['pdfkit']

""" Override pdfkit library's to_pdf method used for converitng file to pdf.
    This is needed because this library doesn't supress the cmd window of wkhtmltopdf.
    Also routing .
"""
def to_pdf_override(self, path=None):
    args = self.command(path)

    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)

    # If the source is a string then we will pipe it into wkhtmltopdf.
    # If we want to add custom CSS to file then we read input file to
    # string and prepend css to it and then pass it to stdin.
    # This is a workaround for a bug in wkhtmltopdf (look closely in README)
    if self.source.isString() or (self.source.isFile() and self.css):
        input = self.source.to_s().encode('utf-8')
    elif self.source.isFileObj():
        input = self.source.source.read().encode('utf-8')
    else:
        input = None
    stdout, stderr = result.communicate(input=input)
    stderr = stderr or stdout
    try:
        stderr = stderr.decode('utf-8')
    except UnicodeDecodeError:
        stderr = ''
    exit_code = result.returncode

    if 'cannot connect to X server' in stderr:
        raise IOError('%s\n'
                      'You will need to run wkhtmltopdf within a "virtual" X server.\n'
                      'Go to the link below for more information\n'
                      'https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server' % stderr)

    if 'Error' in stderr:
        raise IOError('wkhtmltopdf reported an error:\n' + stderr)

    if exit_code != 0:
        raise IOError("wkhtmltopdf exited with non-zero code {0}. error:\n{1}".format(exit_code, stderr))

    # Since wkhtmltopdf sends its output to stderr we will capture it
    # and properly send to stdout
    if '--quiet' not in args:
        sys.stdout.write(stderr)

    if not path:
        return stdout
    else:
        try:
            with codecs.open(path, encoding='utf-8') as f:
                # read 4 bytes to get PDF signature '%PDF'
                text = f.read(4)
                if text == '':
                    raise IOError('Command failed: %s\n'
                                  'Check whhtmltopdf output without \'quiet\' '
                                  'option' % ' '.join(args))
                return True
        except IOError as e:
            raise IOError('Command failed: %s\n'
                          'Check whhtmltopdf output without \'quiet\' option\n'
                          '%s ' %(' '.join(args)),e)


if sys.platform == "win32":
    pdfkit.PDFKit.to_pdf = to_pdf_override
