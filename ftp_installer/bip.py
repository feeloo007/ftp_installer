#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import traceback

from colorama import Fore

import inspect

import functools

def bip( fct ):

    @functools.wraps( fct )
    
    def wrapped( *args, **kwargs ):

        bip_message = ''.join( ' ' for i in range( len( traceback.format_stack() ) ) )

        bip_message += '%s(%s, %s)' % ( fct.__name__, args, kwargs )

        print( Fore.YELLOW + bip_message + Fore.RESET )

        result = fct( *args, **kwargs )

        bip_message += ' = %s' % ( result )

        print( Fore.BLUE + bip_message + Fore.RESET )

        return result
    
    return wrapped 

def add_bip_to_all_methods( cl ):

    origin_init = cl.__init__

    @bip
    def __init__( self, *args, **kwargs ):

        origin_init(
            self,
            *args,
            **kwargs
        )

        for mth in [ 
                        member[ 0 ] 
                        for member in inspect.getmembers( cl ) 
                        if inspect.ismethod( getattr( cl, member[ 0 ] ) )
                   ]:

            setattr( cl, mth, bip( getattr( cl, mth ) ) )

    cl.__init__ = __init__

    return cl
