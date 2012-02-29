#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import os.path
import virtual_map
import bip
import functools


# Structure deavnt contenir :
#     en cle, un module
#     en valeur, un dictionnaire
#     ce second niveau de dictionnaire contient
#         en cle, le nom d'une fonction de os
#         en valeur, un tuple a 2 entrees
#             - la premier entree est la fonction portant ce nom dans os
#             - la seconde entree est la fonction virtual la remplacant
#     on alimente cette structure via le decorator add_to_d_fcts_for_module
__d_fcts_for_module = {}


def add_to_d_fcts_for_module( m ):

     __d_fcts_for_module.setdefault( m, {} )

     def wrapper( fct ):

         assert( not __d_fcts_for_module[ m ].has_key( fct.__name__ ) ), u'La fonction a deja ete ecrasee'

         __d_fcts_for_module[ m ][ fct.__name__ ] = ( getattr( m, fct.__name__ ), fct )

         return fct

     return wrapper


def swith_to_virtual_module( switched_to_virtual_os = False ):
    """
       Decorator a ajouter a une methode pour utiliser automatique 
       la version virtuel de os
    """

    def wrapper( fct ):

        @functools.wraps( fct )

        def wrapped( *args, **kwargs ):

            swith = -1

            if switched_to_virtual_os:
                swith = 1
            else:
                swith = 0

            d_old_fcts_for_module = {}

            for m, d_fcts in __d_fcts_for_module.items():

                for fct_name in d_fcts.keys(): 

                    d_old_fcts_for_module.setdefault( m, {} ).setdefault( fct_name, getattr( m, fct_name ) )

                    setattr( m, fct_name, __d_fcts_for_module[ m ][ fct_name ][ swith ] )

            result = fct( *args, **kwargs )

            for m, d_fcts in __d_fcts_for_module.items():

                for fct_name in d_fcts.keys(): 

                    setattr( m, fct_name, d_old_fcts_for_module[ m ][ fct_name ] )

            return result

        return wrapped

    return wrapper


__virtual_map = virtual_map.VirtualMap()
   
@add_to_d_fcts_for_module( os )
@bip.bip
def getcwd():
    return '/'


@add_to_d_fcts_for_module( os )
@bip.bip
def listdir( path ):
    """
       Version virtual de listdir
    """

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:
        return dirs
    elif is_virtual and is_remote:
        assert( False ), u'A implementer'
    else:
        return []


@add_to_d_fcts_for_module( os )
@bip.bip
def lstat( path ):
    """
       Version virtual de lstat
    """

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( '/home/cloudmgr/.emptydir' )
 
    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        return ''


@add_to_d_fcts_for_module( os )
@bip.bip
def chdir( path ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return 

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:
        __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( path )


@add_to_d_fcts_for_module( os.path )
@bip.bip
def isdir( path ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return True

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( path )
