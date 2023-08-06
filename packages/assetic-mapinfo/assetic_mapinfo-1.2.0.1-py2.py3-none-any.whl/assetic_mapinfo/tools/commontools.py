# coding: utf-8
"""
    assetic_mapinfo.tools.commontools  (commontools.py)
    Tools to assist with using arcgis integration with assetic
"""
from __future__ import absolute_import

import six
import logging


class CommonTools(object):
    """
    Class of tools to support app
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def new_message(self, message, typeid=None):
        """
        Create a message dialogue for user if desktop, else print message
        :param message: the message string for the user
        :param typeid: the type of dialog.  Integer.  optional,Default is none
        :returns: The dialog response as a unicode string, or None
        """
        res = None
        self.logger.info("Assetic Integration: {0}".format(message))
        return res
