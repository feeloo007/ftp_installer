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

import os_from_remote

import pprint

from colorama import Fore

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

__BYPASS_CALL_TO_REAL = '%s_bypass_call_to_real' % ( __name__ )


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


PATH_TO_VIRTUAL_PATH 		= 'path_to_virtual_stats'
PATH_TO_BROKEN_PATH 		= 'path_to_broken_stats'
PATH_TO_UNAVAILABLE_PATH 	= 'path_to_unavaible_path'
PATH_TO_UNAUTHORIZED_PATH 	= 'path_to_unauthorized_path'

PATH_PARAMS			= '%s_PATH_PARAMS'	% __name__

__REAL_CALL			= 0
__VIRTUAL_CALL			= 1
__REMOTE_CALL			= 2

def has_virtual_params( fct ):

    @functools.wraps( fct )
    def wrapped( *args, **kwargs ):

        assert( 
            kwargs.has_key( PATH_PARAMS ) 
        )	, u'kwargs ne contient pas %s' % PATH_PARAMS

        assert( 
            kwargs[ PATH_PARAMS ].has_key( PATH_TO_VIRTUAL_PATH ) 
        )	, u'kwargs[ %s ] ne contient pas %s %s' % ( PATH_PARAMS, PATH_TO_VIRTUAL_PATH, kwargs )

        assert(
            kwargs[ PATH_PARAMS ].has_key( PATH_TO_BROKEN_PATH )
        )       , u'kwargs[ %s ] ne contient pas %s %s' % ( PATH_PARAMS, PATH_TO_BROKEN_PATH, kwargs )

        assert( 
            kwargs[ PATH_PARAMS ].has_key( PATH_TO_UNAVAILABLE_PATH ) 
        )	, u'kwargs ne contient pas %s' % ( PATH_PARAMS, PATH_TO_UNAVAILABLE_PATH, kwargs )

        assert( 
            kwargs[ PATH_PARAMS ].has_key( PATH_TO_UNAUTHORIZED_PATH ) 
        )	, u'kwargs ne contient pas %s' % ( PATH_PARAMS, PATH_TO_UNAUTHORIZED_PATH, kwargs )

        return fct( *args, **kwargs )

    return wrapped

__virtual_map = virtual_map.VirtualMap()



def add_to_d_fcts_for_module( m ):

     __d_fcts_for_module.setdefault( m, {} )

     def wrapper( fct ):

         assert( not __d_fcts_for_module[ m ].has_key( fct.__name__ ) ), u'La fonction a deja ete enregistree'

         def wrapper_to_remote_call( *args, **kwargs ):

             return os_from_remote.remote_call( *args, m = m, fct = fct, **kwargs )

         __d_fcts_for_module[ m ][ fct.__name__ ] = ( 
             bip.bip(
                 getattr( 
                     m, 
                     fct.__name__ 
                 )
             )
             ,
             has_virtual_params(
                 bip.bip(  
                      fct
                 ) 
             ),
             bip.bip(
                 wrapper_to_remote_call
             )
         )

         @functools.wraps( fct )
         def wrapped( *args, **kwargs ):

             f 			= inspect.currentframe( 0 )
             d_virtual_params	= {}

             try:
                 while f:
                     for function_ in ( f.f_globals.get( f.f_code.co_name ), f.f_locals.get( 'fct' ) ):
                        
                         if type( function_ ) == types.FunctionType or type( function_ ) == types.MethodType:

                             if __d_le_has_bypass_call_to_real[ type( function_ ) ]( function_ ):
                                 d_virtual_params = __d_le_get_d_virtual_params[ type( function_ ) ]( function_ )
                                 raise

                     f = f.f_back
             except:
                 pass
             finally:
                 del f

             if d_virtual_params:
                  kwargs.update( { PATH_PARAMS: d_virtual_params } ) 
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ __VIRTUAL_CALL ]( *args, **kwargs )
             else:
                  return __d_fcts_for_module[ m ][ fct.__name__ ][ __REAL_CALL ]( *args, **kwargs )

         setattr( m, fct.__name__, wrapped )

     return wrapper



def bypass_call_to_real( fct, d_virtual_params = { PATH_TO_VIRTUAL_PATH: '/home/cloudmgr/.witnessdir/VIRTUAL', PATH_TO_BROKEN_PATH: '/home/cloudmgr/.witnessdir/BROKEN', PATH_TO_UNAVAILABLE_PATH: '/home/cloudmgr/.witnessdir/UNAVAILABLE', PATH_TO_UNAUTHORIZED_PATH: '/home/cloudmgr/.witnessdir/UNAVAILABLE/UNAUTHORIZED' } ):

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

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    # Cas d'un appel a une ressource virtuelle de l'arborescence
    # Le retour utilise est l'ensemble des fils de niveau inferieur
    # qui sont contenus dans les cles de d_infos[ virtual_map.VirtualMap.INFOS ]
    if is_virtual and not is_remote:

        return [ dir.encode( 'ascii' ) for dir in d_infos[ virtual_map.VirtualMap.INFOS ].keys() ]

    # Cas d'un appel a une ressource remote
    # on
    # utilise la fonction lstats en version remote
    # en completant avec les variables necessaires
    # a la connexion remote et en utilisant
    # virtual_map.VirtualMap.REMOTE_PATH_SEGMENT comme
    # path
    elif is_virtual and is_remote:

        remote_kwargs = kwargs.copy()
        remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

        try:

            return __d_fcts_for_module[ os ][ 'listdir' ][ __REMOTE_CALL ]( 
                d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ], 
                *args, 
                **remote_kwargs 
            )  

        except:

            return __d_fcts_for_module[ os ][ 'listdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAVAILABLE_PATH ] )

    else:
    # Cas d'un path hors arborescence virtuelle ou remote
    # Une exception est levee

        return __d_fcts_for_module[ os ][ 'listdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )


@add_to_d_fcts_for_module( os )
def lstat( path, *args, **kwargs ):
    """
       Version virtual de lstat
    """

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    # Cas d'un appel a une ressource virtuelle de l'arborescence
    # La fonction lstat appelee est celle du systeme en pointant
    # sur PATH_TO_VIRTUAL_PATH
    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'lstat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_VIRTUAL_PATH ] )
 
    # Cas d'un appel a une ressource remote de l'arborescence
    elif is_virtual and is_remote:
        remote_kwargs = kwargs.copy()
        remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

        # Si le chemin remote demande est None, alors on utilise
        # la fonction lstats du systeme en pointant
        # sur PATH_TO_VIRTUAL_PATH
        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            try:

                __d_fcts_for_module[ os ][ 'listdir' ][ __REMOTE_CALL ](
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ],
                    *args,
                    **remote_kwargs
                )

            except:

                return __d_fcts_for_module[ os ][ 'lstat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAVAILABLE_PATH ] )

            return __d_fcts_for_module[ os ][ 'lstat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_VIRTUAL_PATH ] )


        # Si le chemin remote demande n'est pas Non, alors on
        # utilise la fonction lstats en version remote 
        # en completant avec les variables necessaires
        # a la connexion remote et en utilisant
        # virtual_map.VirtualMap.REMOTE_PATH_SEGMENT comme
        # path
        else :

            try:

                return __d_fcts_for_module[ os ][ 'lstat' ][ __REMOTE_CALL ](
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ],
                    *args,
                    **remote_kwargs
                )

            except:

                return __d_fcts_for_module[ os ][ 'lstat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAVAILABLE_KEYS ] )


    # La ressouces demandes n'est pas virtuel
    # On genere une erreur en utilisant un repertoire
    # qui n'existe pas
    else:
        
        return __d_fcts_for_module[ os ][ 'lstat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )


@add_to_d_fcts_for_module( os )
def stat( path, *args, **kwargs ):
    """
       Version virtual de stat
    """

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    # Cas d'un appel a une ressource virtuelle de l'arborescence
    # La fonction stat appelee est celle du systeme en pointant
    # sur PATH_TO_VIRTUAL_PATH
    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'stat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_VIRTUAL_PATH ] )

    # Cas d'un appel a une ressource remote de l'arborescence
    elif is_virtual and is_remote:
        remote_kwargs = kwargs.copy()
        remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

        # Si le chemin remote demande est None, alors on utilise
        # la fonction stats du systeme en pointant
        # sur PATH_TO_VIRTUAL_PATH
        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            try:

                __d_fcts_for_module[ os ][ 'listdir' ][ __REMOTE_CALL ](
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ],
                    *args,
                    **remote_kwargs
                )

            except:

                return __d_fcts_for_module[ os ][ 'stat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAVAILABLE_PATH ] )

            return __d_fcts_for_module[ os ][ 'stat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_VIRTUAL_PATH ] )


        # Si le chemin remote demande n'est pas Non, alors on
        # utilise la fonction stats en version remote
        # en completant avec les variables necessaires
        # a la connexion remote et en utilisant
        # virtual_map.VirtualMap.REMOTE_PATH_SEGMENT comme
        # path
        else :

            try:

                return __d_fcts_for_module[ os ][ 'stat' ][ __REMOTE_CALL ](
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ],
                    *args,
                    **remote_kwargs
                )

            except:

                return __d_fcts_for_module[ os ][ 'stat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAVAILABLE_PATH ] )


    # La ressouces demandes n'est pas virtuel
    # On genere une erreur en utilisant un repertoire
    # qui n'existe pas
    else:

        return __d_fcts_for_module[ os ][ 'stat' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )


@add_to_d_fcts_for_module( os )
def chdir( path, *args, **kwargs ):

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    # Cas d'un path dans l'arborescence virtuelle
    # Le changement de repertoire est accepte
    if is_virtual and not is_remote:

        return 

    elif is_virtual and is_remote:

        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            return

        else:

            remote_kwargs = kwargs.copy()
            remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

            try:

                return __d_fcts_for_module[ os ][ 'chdir' ][ __REMOTE_CALL ]( 
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ], 
                    *args, 
                    **remote_kwargs 
                )

            except:
                return __d_fcts_for_module[ os ][ 'chdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_BROKEN_PATH ] )


    else:

        return __d_fcts_for_module[ os ][ 'chdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_BROKEN_PATH ] )


@add_to_d_fcts_for_module( os.path )
def isdir( path, *args, **kwargs ):

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    # Cas d'un path dans l'arborescence virtuelle
    # Un path virtuel est toujours un repertoire
    if is_virtual and not is_remote:

        return True

    # Cas d'un path dans l'arborescence remote
    # On utilise la fonction isdir en version remote
    # en completant avec les variables necessaires
    # a la connexion remote et en utilisant
    # virtual_map.VirtualMap.REMOTE_PATH_SEGMENT comme
    # path
    elif is_virtual and is_remote:

        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            return True

        else:

            remote_kwargs = kwargs.copy()
            remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

            return __d_fcts_for_module[ os.path ][ 'isdir' ][ __REMOTE_CALL ]( 
                       d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ], 
                       *args, 
                       **remote_kwargs 
                   )

    else:

        return __d_fcts_for_module[ os.path ][ 'isdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )


@add_to_d_fcts_for_module( os )
def mkdir( path, *args, **kwargs ):

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( path )

    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'mkdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )

    elif is_virtual and is_remote:

        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            return __d_fcts_for_module[ os ][ 'mkdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] ) 

        else:

            remote_kwargs = kwargs.copy()
            remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

            try:

                return __d_fcts_for_module[ os ][ 'mkdir' ][ __REMOTE_CALL ](
                    d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ],
                        *args,
                        **remote_kwargs
                    )

            except:

                return __d_fcts_for_module[ os ][ 'mkdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )

    else:

        return __d_fcts_for_module[ os ][ 'mkdir' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )


@add_to_d_fcts_for_module( os )
def open( filename, *args, **kwargs ):

    is_virtual, is_remote, d_infos = __virtual_map.is_virtual( filename )

    # Les parties virtuelles et virtuelles remote racines ne peuvent etre ouvertes
    if is_virtual and not is_remote:

        return __d_fcts_for_module[ os ][ 'open' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )

    elif is_virtual and is_remote:

        if not d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ]:

            __d_fcts_for_module[ os ][ 'open' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )

        else:

            remote_kwargs = kwargs.copy()
            remote_kwargs.update( { os_from_remote.OS_REMOTE_PARAMS: d_infos[ virtual_map.VirtualMap.INFOS ] } )

            f_result = __d_fcts_for_module[ os ][ 'open' ][ __REMOTE_CALL ](
                       d_infos[ virtual_map.VirtualMap.INFOS ][ os_from_remote.ROOT ] + d_infos[ virtual_map.VirtualMap.REMOTE_PATH_SEGMENT ],
                       *args,
                       **remote_kwargs
                   )

            # Dans le cas de l'appel systeme open, on complete le resultat de l'appel
            # remote par le nom de fichier dans la structure purement virtuelle
            f_result.name = filename

            return f_result

    else:

        return __d_fcts_for_module[ os ][ 'open' ][ __REAL_CALL ]( kwargs[ PATH_PARAMS ][ PATH_TO_UNAUTHORIZED_PATH ] )
