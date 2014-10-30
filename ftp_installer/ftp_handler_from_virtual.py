# -*- coding: UTF-8 -*-
from pyftpdlib import handlers

class FTPHandlerFromVirtual(handlers.FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        handlers.FTPHandler.__init__( self, conn, server, ioloop )
        self._current_facts.remove('unique')
