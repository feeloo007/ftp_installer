#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os_from_remote

import json

import pkg_resources


class VirtualMap( object ):

    INFOS 		 	= '%s_infos'			% __name__
    VIRTUAL_PATH_SEGMENT 	= '%s_virtual_path_segment'	% __name__
    REMOTE_PATH_SEGMENT	 	= '%s_remote_path_segment'	% __name__

    __depth_for_remote = 6
    __d_le = {
                 1:   lambda self, appcode                                          		: self.__d[ appcode ],
                 2:   lambda self, appcode, aera                                     		: self.__d[ appcode ][ aera ],
                 3:   lambda self, appcode, aera, env                            		: self.__d[ appcode ][ aera ][ env ],
                 4:   lambda self, appcode, aera, env, appcomp             			: self.__d[ appcode ][ aera ][ env ][ appcomp ],
                 5:   lambda self, appcode, aera, env, appcomp, num_component                  	: self.__d[ appcode ][ aera ][ env ][ appcomp ][ num_component ],
                 6:   lambda self, appcode, aera, env, appcomp, num_component, connections_info	: self.__d[ appcode ][ aera ][ env ][ appcomp ][ num_component ][ connections_info ],
    }

    def __init__( self ):
        
    	self.__d = json.loads( pkg_resources.resource_string( __name__, 'virtual_map.json' ) )


    def get_d( self ):
        return self.__d
    d = property( get_d )

                   
    def is_virtual( self, path ):

        if path == '/':
            return [ 
                       True, 
                       False, 
                       { 
                            VirtualMap.INFOS			: self.__d, 
                            VirtualMap.VIRTUAL_PATH_SEGMENT	: '/', 
                            VirtualMap.REMOTE_PATH_SEGMENT	: '/',
                       } 
                   ]
     
        l_dir = path.split( '/' )[ 1: ]

        try:

            return [ 
                       True, 
                       len( l_dir ) >=  VirtualMap.__depth_for_remote,
                       {
                           VirtualMap.INFOS			: VirtualMap.__d_le[
                                                                      len( l_dir[ :VirtualMap.__depth_for_remote ] )
                                                                  ]( 
                                                                        self, 
                                                                        *l_dir[ :VirtualMap.__depth_for_remote ] 
                                                                   ),
                           VirtualMap.VIRTUAL_PATH_SEGMENT      : '/' + '/'.join( l_dir[ :VirtualMap.__depth_for_remote ] ),
                           VirtualMap.REMOTE_PATH_SEGMENT 	: '' + '/'.join( l_dir[ VirtualMap.__depth_for_remote:: ] ),
                       }
                   ]

        except Exception, e:
            from colorama import Fore
            print( Fore.RED + repr( e  ) + Fore.RESET )
            return [ False, False,  {} ]
        
        return [ False, False, {} ]
