#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import traceback

from colorama import Fore

import inspect

import functools

import pprint

def bip( fct ):

    @functools.wraps( fct )
    
    def wrapped( *args, **kwargs ):

        bip_message = ''
        #####bip_message = ''.join( ' ' for i in range( len( traceback.format_stack() ) ) )

        #bip_message += '%s(%s, %s)' % ( fct.__name__, args, kwargs )

        #print( Fore.YELLOW + bip_message + Fore.RESET )

        result = fct( *args, **kwargs )

        #bip_message += ' = %s' % ( pprint.pformat ( result ) )

        #print( Fore.BLUE + bip_message + Fore.RESET )

        return result

    wrapped.__bipped	= True
    
    return wrapped 

def add_bip_to_all_methods( cl ):
    """
        fonction appliquant à l'ensemble des méthodes
        d'une classe le décorateur bip.
        En coopération avec le décoracteur bip, il n'est pas possible
        d'appliquer 2 fois le décoracteur bip à une méthode qui
        est déjà le résultat du décorateur bip (__bipped).
    """

    for method_name in [
                        member[ 0 ]
                        for member in inspect.getmembers( cl )
                        if inspect.ismethod( getattr( cl, member[ 0 ] ) )
                   ]:

        if not hasattr( getattr( cl, method_name ), '__bipped' ):

            setattr(
                cl,
                method_name,
                bip(
                    getattr(
                        cl,
                        method_name
                    )
                )
            )

    return cl
