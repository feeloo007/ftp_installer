#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import virtual_map

import os_from_virtual_map

import bip

import functools

import ftplib

import ftputil

import os

import os.path

import pprint

from colorama import Fore

import simplejson

LOGIN			= '%s_LOGIN'		% __name__
SERVER      		= '%s_SERVER'		% __name__
PASSWORD		= '%s_PASSWORD' 	% __name__
ROOT			= '%s_ROOT'     	% __name__
OS_REMOTE_PARAMS 	= '%s_OS_REMOTE_PARAMS' % __name__

def has_os_from_remote_params( fct ):

    @functools.wraps( fct )
    def wrapped( *args, **kwargs ):

        assert( 
            kwargs.has_key( OS_REMOTE_PARAMS ) 
        ) , u'kwargs ne contient pas %s %s' 	% ( OS_REMOTE_PARAMS, kwargs )

        assert( 
            kwargs[ OS_REMOTE_PARAMS ].has_key( LOGIN ) 
        ) , u'kwargs[ %s ] ne contient pas %s %s' 	% ( OS_REMOTE_PARAMS, LOGIN, kwargs[ OS_REMOTE_PARAMS ] )

        assert( 
            kwargs[ OS_REMOTE_PARAMS ].has_key( SERVER )
        ) , u'kwargs[ %s ] ne contient pas %s %s'	% ( OS_REMOTE_PARAMS, SERVER, kwargs[ OS_REMOTE_PARAMS ] )

        assert( 
            kwargs[ OS_REMOTE_PARAMS ].has_key( PASSWORD ) 
        ) , u'kwargs[ %s] ne contient pas %s %s' 	%( OS_REMOTE_PARAMS, PASSWORD, kwargs )

        assert( 
            kwargs[ OS_REMOTE_PARAMS ].has_key( ROOT ) 
        ) , u'kwargs[ %s ] ne contient pas %s %s' 	%( OS_REMOTE_PARAMS, ROOT, kwargs )

        return fct( *args, **kwargs )

    return wrapped


def cast_unicode_to_ascii( fct ):
    """
    decorator adressant un problème de compatibilité entre
    pyftpdlib 0.7.0
    et
    ftpuil 3.1
    ftputil 3.1 manipule les données en unicode alors que
    pyftpdlib 0.7.0 les manipule en ascii.
    Sous certaines conditions, les chaines unicode
    altèrent le flux de données de pyftpdlib.
    Par exemple, avec un client filezilla, qui conduit
    à utiliser la méthode _AbstractedFS.format_mlsx
    le fait qu'une partie des attributs du résultat d'un stat
    soit en unicode conduit le système à ne pas pouvoir
    afficher les fichiers.
    On réalise donc un encodage en ascii de ces paramètres.
    Un bug est clairement identifié avec les valeurs issue de stat
    dont les objets sont instanciés depuis la classe :
        ftputil.stat.StatResult
    Pour les attributs st_uid et st_gid.

    Pour un résultat de type unicode, on réalise un transoodage ascii.

    Pour une série d'autre type, on utilise une propriété
    de simplejson.
    On commence par convertir en JSON ascii la structure python (on obtient
    un str plutôt qu'un unicode).
    Puis, on reconverti le str obtenue en structure python
    en la passant en paramètre de la classe de départ.
    Avec un str en entrée, simplejson génére une structure contenant
    uniquement des str et non des unicodes.

    Cette encodage ne sera plus nécessaire à partir des versions de
    pyftpdlib manipulant les données en unicode.
    """

    @functools.wraps( fct )
    def wrapped( *args, **kwargs ):

        res 	= fct( * args, ** kwargs )

        if (
            isinstance( res, unicode )
           ):
            res = res.encode( 'ascii' )

        if (
            isinstance( res, ftputil.stat.StatResult )
            or
            isinstance( res, list )
            or
            isinstance( res, dict )
           ):

            try:

                def _cast_unicode_to_ascii( res ):
                    return res.__class__(
                        simplejson.loads(
                            simplejson.dumps(
                                res
                                ,
                                encoding = "ascii"
                            )
                        )
                    )

                res = _cast_unicode_to_ascii( res )

            except Exception, e:
                print e

        return res

    return wrapped

class OsRemoteFTPSession( ftplib.FTP ):
    def __init__( self, host, userid, password ):
        """Act like ftplib.FTP's constructor but connect to another port."""
        ftplib.FTP.__init__( self )
        self.connect( host )
        self.login( userid, password )
        self.set_pasv( True )

__d_ftp_clients = {}

@bip.bip
@cast_unicode_to_ascii
@has_os_from_remote_params
def remote_call( *args, **kwargs ):

        assert( kwargs.has_key( 'm' ) ), u'm n\' a pas ete transmis. Impossible de continuer'
        assert( kwargs.has_key( 'fct' ) ), u'fct n\' a pas ete transmis. Impossible de continuer'

        ftp_params = (
            kwargs[ OS_REMOTE_PARAMS ][ SERVER ],
            kwargs[ OS_REMOTE_PARAMS ][ LOGIN ],
            kwargs[ OS_REMOTE_PARAMS ][ PASSWORD ],
        )

        client_key = ( 
            ftp_params[ 0 ],
            ftp_params[ 1 ],
            ftp_params[ 2 ],
        )

        kwargs_for_remote = kwargs.copy()
        del( kwargs_for_remote[ 'm' ] )
        del( kwargs_for_remote[ 'fct' ] )
        del( kwargs_for_remote[ OS_REMOTE_PARAMS ] )
        del( kwargs_for_remote[ os_from_virtual_map.PATH_PARAMS ] )

        # Recreation du client si la connexion est closed
        if not __d_ftp_clients.has_key( client_key ):
            __d_ftp_clients[ client_key ] = ftputil.FTPHost( *ftp_params, session_factory = OsRemoteFTPSession )

        if __d_ftp_clients[ client_key ].closed:
            __d_ftp_clients[ client_key ] = ftputil.FTPHost( *ftp_params, session_factory = OsRemoteFTPSession )

        try:

            if kwargs[ 'm' ] == os:
        
                return getattr(
                    __d_ftp_clients[ client_key ],
                    kwargs[ 'fct' ].__name__
                )( *args, **kwargs_for_remote )

            elif kwargs[ 'm' ] == os.path:

                return getattr(
                    __d_ftp_clients[ client_key ].path,
                    kwargs[ 'fct' ].__name__
                )( *args, **kwargs_for_remote )

        except:
            # Relancement de la commande
            # Lors d'une premiere exception
            # Ceci peut-etre du a un inactivite de
            # 10 minutes 
            # Si une exception a lieu de nouveau
            # Elle est transmise  
            try:
                __d_ftp_clients[ client_key ] = ftputil.FTPHost( *ftp_params, session_factory = OsRemoteFTPSession )

                if kwargs[ 'm' ] == os:

                    return getattr(
                        __d_ftp_clients[ client_key ],
                        kwargs[ 'fct' ].__name__
                    )( *args, **kwargs_for_remote )

                elif kwargs[ 'm' ] == os.path:

                    return getattr(
                        __d_ftp_clients[ client_key ].path,
                        kwargs[ 'fct' ].__name__
                    )( *args, **kwargs_for_remote )

            except: 
                raise
