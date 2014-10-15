#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from pyftpdlib                  import ftpserver

import bip

import os

import inspect

# Chargement du module ecrasant les fonctions de os
import os_from_virtual_map


@bip.add_bip_to_all_methods
@os_from_virtual_map.add_bypass_call_to_real(
    [
                 'listdir'
                 ,
                 'get_list_dir'
                 ,
                 'isdir'
                 ,
                 'isfile'
                 ,
                 'format_list'
                 ,
                 'format_mlsx'
                 ,
                 'stat'
                 ,
                 'lstat'
                 ,
                 'lexists'
                 ,
                 'chdir'
                 ,
                 'mkdir'
                 ,
                 'open'
                 ,
                 'rmdir'
                 ,
                 'remove'
                 ,
                 'rename'
                 ,
    ]
)
class FTPInstallerAbstractedFS( ftpserver.AbstractedFS ):

    def __init__(self, root, cmd_channel):
        """
         - (str) root: the user "real" home directory (e.g. '/home/user')
         - (instance) cmd_channel: the FTPHandler class instance
        """
        # Set initial current working directory.
        # By default initial cwd is set to "/" to emulate a chroot jail.
        # If a different behavior is desired (e.g. initial cwd = root,
        # to reflect the real filesystem) users overriding this class
        # are responsible to set _cwd attribute as necessary.

        ftpserver.AbstractedFS.__init__( self, '/home/cloudmgr/.witnessdir', cmd_channel )

    def ftp2fs(self, ftppath ):

        return self.ftpnorm( ftppath )

    def fs2ftp(self, fspath ):

        return self.ftpnorm( fspath )

    def validpath( self, path ):

        return True

    def get_user_by_uid( self, uid ):

        return 'cloudmgr'

    def get_group_by_gid( self, gid ):

        return 'cloudmgr'

    def open( self, filename, *args, **kwargs ):
     
        return os.open( filename, *args, **kwargs )
