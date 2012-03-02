#!/usr/bin/env python
# -*- coding: UTF-8 -*-
class VirtualMap( object ):

    INFOS 		 	= 'infos' 
    VIRTUAL_PATH_SEGMENT 	= 'virtual_path_segment' 
    REMOTE_PATH_SEGMENT	 	= 'remote_path_segment' 

    __depth_for_remote = 6
    __d_le = {
                 1:   lambda self, appcode                                          			: self.__d[ appcode ],
                 2:   lambda self, appcode, env                                     			: self.__d[ appcode ][ env ],
                 3:   lambda self, appcode, env, appcomp                            			: self.__d[ appcode ][ env ][ appcomp ],
                 4:   lambda self, appcode, env, appcomp, num_component             			: self.__d[ appcode ][ env ][ appcomp ][ num_component ],
                 5:   lambda self, appcode, env, appcomp, num_component, aera                  		: self.__d[ appcode ][ env ][ appcomp ][ num_component ][ aera ],
                 6:   lambda self, appcode, env, appcomp, num_component, aera, connections_info 	: self.__d[ appcode ][ env ][ appcomp ][ num_component ][ aera ][ connections_info ],
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
            return [ 
                       True, 
                       False, 
                       { 
                            VirtualMap.INFOS			: self.__d, 
                            VirtualMap.VIRTUAL_PATH_SEGMENT	: '/', 
                            VirtualMap.REMOTE_PATH_SEGMENT	: None 
                       } 
                   ]
     
        l_dir = path.split( '/' )[ 1: ]

        try:

            return [ 
                       True, 
                       len( l_dir ) >  VirtualMap.__depth_for_remote,
                       {
                           VirtualMap.INFOS			: VirtualMap.__d_le[
                                                                      len( l_dir[ :VirtualMap.__depth_for_remote ] )
                                                                  ]( 
                                                                        self, 
                                                                        *l_dir[ :VirtualMap.__depth_for_remote ] 
                                                                   ),
                           VirtualMap.VIRTUAL_PATH_SEGMENT      : l_dir[ :VirtualMap.__depth_for_remote ],
                           VirtualMap.REMOTE_PATH_SEGMENT 	: l_dir[ VirtualMap.__depth_for_remote:: ],
                       }
                   ]

        except Exception, e:
            from colorama import Fore
            print( Fore.RED + repr( e  ) + Fore.RESET )
            return [ False, False,  {} ]
        
        return [ False, False, {} ]
