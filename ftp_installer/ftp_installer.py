# -*- coding: UTF-8 -*-
from pyftpdlib 			import servers
from pyftpdlib 			import handlers
from pyftpdlib 			import authorizers
from ftp_handler_from_virtual	import FTPHandlerFromVirtual
from ftp_installer_abstractedfs import FTPInstallerAbstractedFS

def main():
    authorizer = authorizers.DummyAuthorizer()
    
    authorizer.add_user( 
        u'test',
        password	= u'test',
        homedir 	= u'/home/cloudmgr/.witnessdir',
        perm		= u'elradfmw'
    )

    handler 			= FTPHandlerFromVirtual
    handler.authorizer 		= authorizer
    handler.abstracted_fs 	= FTPInstallerAbstractedFS

    address = ( 
                  '10.161.113.60', 
                  2121 
              )

    server = servers.FTPServer(
                 address, 
                 handler 
             )

    server.serve_forever()

if __name__ == '__main__':
    main()
