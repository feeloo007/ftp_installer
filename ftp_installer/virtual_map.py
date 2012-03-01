#!/usr/bin/env python
# -*- coding: UTF-8 -*-
class VirtualMap( object ):

    __max_keys = 5
    __d_le = {
                 1:   lambda self, appcode                                          : self.__d[ appcode ],
                 2:   lambda self, appcode, env                                     : self.__d[ appcode ][ env ],
                 3:   lambda self, appcode, env, appcomp                            : self.__d[ appcode ][ env ][ appcomp ],
                 4:   lambda self, appcode, env, appcomp, num_component             : self.__d[ appcode ][ env ][ appcomp ][ num_component ],
                 5:   lambda self, appcode, env, appcomp, num_component, aera       : self.__d[ appcode ][ env ][ appcomp ][ num_component ][ aera ],
    }

    def __init__( self ):
        
        self.__d = {
                    'X04': {
                            'R7': { 
                                   'TOMCAT': {
                                              '0001': {
                                                       'VILLE': {
                                                                 'WEBAPP_INSTALLER': {
                                                                                      'LOGIN': 		'X04_0001_WEBAPP_INSTALLER',
                                                                                      'SERVER':		'X04-R7-TOMCAT-0001-VILLE',
                                                                                      'PASSWORD': 	'X04_0001_WEBAPP_INSTALLER',
                                                                                      'ROOT':		'/',
                                                                                     },
                                                                 'WEBAPP_RO': {
                                                                               'LOGIN':          'X04_0001_WEBAPP_RO',
                                                                               'SERVER':         'X04-R7-TOMCAT-0001-VILLE',
                                                                               'PASSWORD':       'X04_0001_WEBAPP_RO',
                                                                               'ROOT':           '/',
                                                                              },
                                                                 'DATAS': {
                                                                           'LOGIN': 		'X04_0001_WEBAPP_INSTALLER',
                                                                           'SERVER':		'X04-R7-TOMCAT-0001-VILLE',
                                                                           'PASSWORD': 		'X04_0001_WEBAPP_INSTALLER',
                                                                           'ROOT':		'/',
                                                                          },
                                                                }
                                                      },
                                              '0002': {
                                                       'VILLE': {
                                                                 'WEBAPP_INSTALLER': {
                                                                                      'LOGIN': 		'X01_0002_WEBAPP_INSTALLER',
                                                                                      'SERVER':		'X04-R7-TOMCAT-0001-VILLE',
                                                                                      'PASSWORD': 	'X01_0002_WEBAPP_INSTALLER',
                                                                                      'ROOT':		'/',
                                                                                     },
                                                                 'WEBAPP_RO': {
                                                                               'LOGIN':          'X04_0002_WEBAPP_RO',
                                                                               'SERVER':         'X04-R7-TOMCAT-0002-VILLE',
                                                                               'PASSWORD':       'X04_0002_WEBAPP_RO',
                                                                               'ROOT':           '/',
                                                                              },
                                                                 'DATAS': {
                                                                           'LOGIN': 		'X04_0002_WEBAPP_INSTALLER',
                                                                           'SERVER':		'X04-R7-TOMCAT-0002-VILLE',
                                                                           'PASSWORD': 		'X04_0002_WEBAPP_INSTALLER',
                                                                           'ROOT':		'/',
                                                                          },
                                                                }
                                                      }
                                             }
                                  }
                           }
                   }

                   
    def is_virtual( self, path ):

        if path == '/':
            return [ True, False, self.__d.keys() ]
     
        l_dir = path.split( '/' )[ 1: ]

        try:

            return [ 
                       True, 
                       len( l_dir ) >  VirtualMap.__max_keys,
                       VirtualMap.__d_le[
                                              min(
                                                      len( l_dir ),
                                                      VirtualMap.__max_keys
                                                 )
                                        ]( self, *l_dir ).keys()
                   ]

        except Exception, e:
            from colorama import Fore
            print( Fore.RED + repr( e  ) + Fore.RESET )
            return [ False, False,  [ 'REMOTE' ] ]
        
        return [ False, False, [] ]
