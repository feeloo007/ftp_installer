#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import os.path
import virtual_map
import bip
import functools

import inspect

import types

import errno


# Structure devant contenir :
#     en cle, un module
#     en valeur, un dictionnaire
#     ce second niveau de dictionnaire contient
#         en cle, le nom d'une fonction de os
#         en valeur, un tuple a 2 entrees
#             - la premier entree est la fonction portant ce nom dans os
#             - la seconde entree est la fonction virtual la remplacant
#     on alimente cette structure via le decorator add_to_d_fcts_for_module
__d_fcts_for_module = {}

__BYPASS_CALL_TO_REAL = '__bypass_call_to_real'


__d_le_set_bypass_call_to_real = {
    types.MethodType    : lambda fct: setattr( fct.im_func      , __BYPASS_CALL_TO_REAL, True ),
    types.FunctionType  : lambda fct: setattr( fct              , __BYPASS_CALL_TO_REAL, True ),
}

__d_le_has_bypass_call_to_real = {
    types.MethodType    : lambda fct: hasattr( fct.im_func      , __BYPASS_CALL_TO_REAL ),
    types.FunctionType  : lambda fct: hasattr( fct              , __BYPASS_CALL_TO_REAL ),
    types.NoneType	: lambda fct: False,
}

__d_le_get_bypass_call_to_real = {
    types.MethodType    : lambda fct: getattr( fct.im_func      , __BYPASS_CALL_TO_REAL ),
    types.FunctionType  : lambda fct: getattr( fct              , __BYPASS_CALL_TO_REAL ),
    types.NoneType      : lambda fct: False,
}


def add_to_d_fcts_for_module( m ):

     __d_fcts_for_module.setdefault( m, {} )

     def wrapper( fct ):

         assert( not __d_fcts_for_module[ m ].has_key( fct.__name__ ) ), u'La fonction a deja ete enregistree'

         __d_fcts_for_module[ m ][ fct.__name__ ] = ( getattr( m, fct.__name__ ), fct )

         @functools.wraps( fct )
         def wrapped( *args, **kwargs ):

             f 			= inspect.currentframe( 1 )
             real_call_bypassed	= None

             try:
                 while f:
                     for function_ in ( f.f_globals.get( f.f_code.co_name ), f.f_locals.get( 'fct' ) ):

                         if __d_le_has_bypass_call_to_real[ type( function_ ) ]( function_ ):
                             real_call_bypassed = __d_le_get_bypass_call_to_real[ type( function_ ) ]( function_ )
                             raise

                     f = f.f_back
             except:
                 pass
             finally:
                 del f

             if real_call_bypassed:
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ 1 ]( *args, **kwargs )
             else:
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ 0 ]( *args, **kwargs )

         setattr( m, fct.__name__, wrapped )

     return wrapper




def bypass_call_to_real( fct ):

     __d_le_set_bypass_call_to_real[ type( fct ) ]( fct )

     return fct
          

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

        raise


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

        return __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( '/home/cloudmgr/.emptydir/BROKEN' )


@add_to_d_fcts_for_module( os )
@bip.bip
def chdir( path ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return 

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        raise OSError( errno.ENOENT, path )


@add_to_d_fcts_for_module( os.path )
@bip.bip
def isdir( path ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return True

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        #return __d_fcts_for_module[ os.path ][ 'isdir' ][ 0 ]( '/home/cloudmgr/.emptydir/BROKEN' )
        return False
