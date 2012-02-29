# -*- coding: UTF-8 -*-
from pyftpdlib 			import ftpserver
from ftp_installer_abstractedfs import FTPInstallerAbstractedFS

def main():
    authorizer = ftpserver.DummyAuthorizer()
    
    authorizer.add_user( 
        'test', 
        password	= 'test', 
        homedir 	= '.', 
        perm		= 'elradfmw' 
    )

    handler 			= ftpserver.FTPHandler
    handler.authorizer 		= authorizer
    handler.abstracted_fs 	= FTPInstallerAbstractedFS

    address = ( 
                  '10.161.113.60', 
                  2121 
              )

    server = ftpserver.FTPServer( 
                 address, 
                 handler 
             )

    server.serve_forever()

if __name__ == '__main__':
    main()
