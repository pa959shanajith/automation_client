#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      prudhvi.gujjuboyina
#
# Created:     22-02-2017
# Copyright:   (c) prudhvi.gujjuboyina 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import ninteen_68_desktop_scrape

import logger

launchobj=ninteen_68_desktop_scrape.obj


class highLight():

    def highLiht_element(self,objname,parent,*args):

        logger.print_on_console('Highlight Object: ' +objname)
        print launchobj
        status=launchobj.higlight(objname,parent,*args)
        logger.print_on_console(objname+"  Highlight Status "+str(status))





