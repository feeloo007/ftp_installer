# -*- coding: UTF-8 -*-
# --- filesystem

from contextlib     import closing
from fabric.network import connect

def deal_with_ftppath( fct ):

    d = {}

    def wrapper( self, *args, **kwargs ):

        print 'wrapper'
        print kwargs

        with closing( connect( 'cloudmgr', '127.0.0.1', 22 ) ) as ssh:
            with closing( ssh.open_sftp() ) as sftp:
               return fct( self, os = sftp, *args, **kwargs )

    return wrapper


class Test( object ):

    def __init__( self ):
       pass

    @deal_with_ftppath
    def ftpnorm(self, ftppath, os = None ):
        """Normalize a "virtual" ftp pathname (tipically the raw string
        coming from client) depending on the current working directory.

        Example (having "/foo" as current working directory):
        >>> ftpnorm('bar')
        '/foo/bar'

        Note: directory separators are system independent ("/").
        Pathname returned is always absolutized.
        """
        print '%s( %s )' % ( self.ftpnorm, ftppath )
        if os.path.isabs(ftppath):
            p = os.path.normpath(ftppath)
        else:
            p = os.path.normpath(os.path.join(self.cwd, ftppath))
        # normalize string in a standard web-path notation having '/'
        # as separator.
        p = p.replace("\\", "/")
        # os.path.normpath supports UNC paths (e.g. "//a/b/c") but we
        # don't need them.  In case we get an UNC path we collapse
        # redundant separators appearing at the beginning of the string
        while p[:2] == '//':
            p = p[1:]
        # Anti path traversal: don't trust user input, in the event
        # that self.cwd is not absolute, return "/" as a safety measure.
        # This is for extra protection, maybe not really necessary.
        if not os.path.isabs(p):
            p = "/"
        return p
