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
    types.MethodType    : lambda fct, d_virtual_params: setattr( fct.im_func      , __BYPASS_CALL_TO_REAL, d_virtual_params ),
    types.FunctionType  : lambda fct, d_virtual_params: setattr( fct              , __BYPASS_CALL_TO_REAL, d_virtual_params ),
}

__d_le_has_bypass_call_to_real = {
    types.MethodType    : lambda fct: hasattr( fct.im_func      , __BYPASS_CALL_TO_REAL ),
    types.FunctionType  : lambda fct: hasattr( fct              , __BYPASS_CALL_TO_REAL ),
    types.NoneType	: lambda fct: False,
}

__d_le_get_d_virtual_params = {
    types.MethodType    : lambda fct: getattr( fct.im_func      , __BYPASS_CALL_TO_REAL ),
    types.FunctionType  : lambda fct: getattr( fct              , __BYPASS_CALL_TO_REAL ),
    types.NoneType      : lambda fct: False,
}


PATH_TO_CHROOT 		= 'path_to_chroot'
PATH_TO_BROKEN_PATH 	= 'path_to_broken_path'
def has_virtual_params( fct ):

    @functools.wraps( fct )
    def wrapped( *args, **kwargs ):

        assert( kwargs.has_key( PATH_TO_CHROOT ) )		, u'kwargs ne contient pas %s' % PATH_TO_CHROOT
        assert( kwargs.has_key( PATH_TO_BROKEN_PATH ) )		, u'kwargs ne contient pas %s' % PATH_TO_BROKEN_PATH

        return fct( *args, **kwargs )

    return wrapped

__virtual_map = virtual_map.VirtualMap()

def add_to_d_fcts_for_module( m ):

     __d_fcts_for_module.setdefault( m, {} )

     def wrapper( fct ):

         assert( not __d_fcts_for_module[ m ].has_key( fct.__name__ ) ), u'La fonction a deja ete enregistree'

         __d_fcts_for_module[ m ][ fct.__name__ ] = ( 
             getattr( 
                 m, 
                 fct.__name__ 
             ),
             has_virtual_params(
                 bip.bip(  
                      fct
                 ) 
             )
         )

         @functools.wraps( fct )
         def wrapped( *args, **kwargs ):

             f 			= inspect.currentframe( 1 )
             d_virtual_params	= {}

             try:
                 while f:
                     for function_ in ( f.f_globals.get( f.f_code.co_name ), f.f_locals.get( 'fct' ) ):

                         if __d_le_has_bypass_call_to_real[ type( function_ ) ]( function_ ):
                             d_virtual_params = __d_le_get_d_virtual_params[ type( function_ ) ]( function_ )
                             raise

                     f = f.f_back
             except:
                 pass
             finally:
                 del f

             if d_virtual_params:
                  kwargs.update( d_virtual_params ) 
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ 1 ]( *args, **kwargs )
             else:
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ 0 ]( *args, **kwargs )

         setattr( m, fct.__name__, wrapped )

     return wrapper



def bypass_call_to_real( fct, d_virtual_params = { PATH_TO_CHROOT: '/home/cloudmgr/.emptydir', PATH_TO_BROKEN_PATH: '/home/cloudmgr/.emptydir/BROKEN' } ):

     __d_le_set_bypass_call_to_real[ type( fct ) ]( fct, d_virtual_params )

     return fct


   
@add_to_d_fcts_for_module( os )
def getcwd( *args, **kwargs ):

    return '/'


@add_to_d_fcts_for_module( os )
def listdir( path, *args, **kwargs ):
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
def lstat( path, *args, **kwargs ):
    """
       Version virtual de lstat
    """

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( kwargs[ PATH_TO_CHROOT ] )
 
    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        return __d_fcts_for_module[ os ][ 'lstat' ][ 0 ]( kwargs[ PATH_TO_BROKEN_PATH ] )


@add_to_d_fcts_for_module( os )
def chdir( path, *args, **kwargs ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return 

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        raise OSError( errno.ENOENT, path )


@add_to_d_fcts_for_module( os.path )
def isdir( path, *args, **kwargs ):

    is_virtual, is_remote, dirs = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return True

    elif is_virtual and is_remote:

        assert( False ), u'A implementer'

    else:

        return False
