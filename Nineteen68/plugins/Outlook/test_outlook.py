#-------------------------------------------------------------------------------
# Name:        PyTest
# Purpose:
#
# Author:      sushma.p
#
# Created:     07-09-2016
# Copyright:   (c) sushma.p 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
import  outlook

## A simple unit  test to test outlook keywords
class outlooktestcase(unittest.TestCase):
    global a
    a=outlook.OutlookKeywords()
    def test_outlook(self):
## Give proper inputs
        fromMail="Skill Central"
        subject="Skill Central - Primary Skill(s) in your profile"
        toMail="Prudhvi Prem Gujjuboyina"

        self.assertTrue(a.switchToFolder('\\prudhvi.gujjuboyina@slkgroup.com\Inbox\test\git\demo'))
## Test the mail
        self.assertTrue(a.GetEmail(fromMail, subject, toMail))
## verify Subject
        self.assertEqual(a.GetSubject(),"Skill Central - Primary Skill(s) in your profile")
## verify from Mail
        self.assertEqual(a.GetFromMailId(),"Social.Business@slkgroup.com")
## verify To Mail
        self.assertEqual(a.GetToMailID(),"Prudhvi Prem Gujjuboyina")
## verify Body
##        self.assertEqual(a.GetBody(),'Hi Prudhvi Prem Gujjuboyina,\r\n\r\nThis is to inform you that the below listed skills have been updated as your primary skills in Skill Central, basis the experience and proficiency level.\r\n\r\n\r\nSkill(s) Details:\r\n\r\n\u2022  SQL\r\n\u2022  Core JAVA\r\n\u2022  JDBC\r\n\r\nYou can review/alter (if required) your Primary skills, by logging on to Skill Central. You can access Skill Central via Converge > Employee Self Service > Skill Central or click here <https://converge/SkillCentral/> \r\n\r\nShould you encounter any difficulties, please write to us on Social.Business@slkgroup.com <mailto:Social.Business@slkgroup.com> \r\n\r\nFrom,\r\nSkill Central')
## verify Attachment status
        self.assertEqual(a.GetAttachmentStatus(),"No")



if __name__ == '__main__':
    unittest.main()

##import unittest
##from prime import is_prime
##
##class PrimesTestCase(unittest.TestCase):
##    """Tests for `primes.py`."""
##
##    def test_is_five_prime(self):
##        """Is five successfully determined to be prime?"""
##        self.assertTrue(is_prime(5))
##
##if __name__ == '__main__':
##    unittest.main()
