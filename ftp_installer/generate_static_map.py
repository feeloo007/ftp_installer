# -*- coding: UTF-8 -*-
import pprint

import string,random

import json

import math

import os
import os.path

letters		= string.ascii_letters+string.digits

d = {}

virtual_map_json_filepath 	= '/var/tmp/virtual_map/virtual_map.json'
virtual_map_login_password 	= '/var/tmp/virtual_map/virtualftpguest'
virtual_map_ftpusers_dir	= '/var/tmp/virtual_map/ftpusers/'
virtual_map_partial_hosts	= '/var/tmp/virtual_map/partial_hosts'

def main():

    partial_hosts 	= ''

    d_appcomp_num_component_to_dir = { 
        ( 'TOMCAT', '0001' )	: [ 'DATAS', 'INSTALLER', 'RO' ], 
        ( 'TOMCAT', '0002' )	: [ 'DATAS', 'INSTALLER', 'RO' ], 
        ( 'TOMCAT', 'FO' )	: [ 'RO' ], 
        ( 'TOMCAT', 'BO' )	: [ 'RO' ], 
        ( 'MYSQL', '0001' )	: [ 'EXECUTABLES', 'DUMPS' ], 
        ( 'MYSQL', '0002' )	: [ 'EXECUTABLES', 'DUMPS' ], 
        ( 'MYSQL', 'FO' )	: [ 'DUMPS' ], 
        ( 'MYSQL', 'BO' )	: [ 'DUMPS' ], 
    }

    d_appcode_2_env_aera_num_comp = {
        'X01': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X02': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X03': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X04': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ), ( 'R7', 'VILLE', '0001'), ( 'R7', 'VILLE', '0002') ],
        'X05': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X06': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X07': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X08': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X09': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X10': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X11': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X12': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X13': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X14': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X15': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X16': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X17': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X18': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X19': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
        'X20': [ ( 'PR', 'DMZ', '0001'), ( 'PR', 'DMZ', '0002'), ( 'PR', 'DMZ', 'BO' ), ( 'PR', 'DMZ', 'FO' ) ],
    }

    d_appcode_to_aera = {
        'X01'	: [ 'DMZ' ],
        'X02'	: [ 'DMZ' ],
        'X03'	: [ 'DMZ' ],
        'X04'	: [ 'DMZ', 'VILLE' ],
        'X05'	: [ 'DMZ' ],
        'X06'	: [ 'DMZ' ],
        'X07'	: [ 'DMZ' ],
        'X08'	: [ 'DMZ' ],
        'X09'	: [ 'DMZ' ],
        'X10'	: [ 'DMZ' ],
        'X11'	: [ 'DMZ' ],
        'X12'	: [ 'DMZ' ],
        'X13'	: [ 'DMZ' ],
        'X14'	: [ 'DMZ' ],
        'X15'	: [ 'DMZ' ],
        'X16'	: [ 'DMZ' ],
        'X17'	: [ 'DMZ' ],
        'X18'	: [ 'DMZ' ],
        'X19'	: [ 'DMZ' ],
        'X20'	: [ 'DMZ' ],
    }

    d_appcode_aera_to_env = {
        ( 'X01', 'DMZ' )	: [ 'PR' ],
        ( 'X02', 'DMZ' )	: [ 'PR' ],
        ( 'X03', 'DMZ' )	: [ 'PR' ],
        ( 'X04', 'DMZ' )	: [ 'PR' ],
        ( 'X04', 'VILLE' )	: [ 'R7' ],
        ( 'X05', 'DMZ' )	: [ 'PR' ],
        ( 'X06', 'DMZ' )	: [ 'PR' ],
        ( 'X07', 'DMZ' )	: [ 'PR' ],
        ( 'X08', 'DMZ' )	: [ 'PR' ],
        ( 'X09', 'DMZ' )	: [ 'PR' ],
        ( 'X10', 'DMZ' )	: [ 'PR' ],
        ( 'X11', 'DMZ' )	: [ 'PR' ],
        ( 'X12', 'DMZ' )	: [ 'PR' ],
        ( 'X13', 'DMZ' )	: [ 'PR' ],
        ( 'X14', 'DMZ' )	: [ 'PR' ],
        ( 'X15', 'DMZ' )	: [ 'PR' ],
        ( 'X16', 'DMZ' )	: [ 'PR' ],
        ( 'X17', 'DMZ' )	: [ 'PR' ],
        ( 'X18', 'DMZ' )	: [ 'PR' ],
        ( 'X19', 'DMZ' )	: [ 'PR' ],
         ('X20', 'DMZ' )	: [ 'PR' ],

    }

    d_appcode_aera_num_component_env_2_ip = {
        ( 'X01', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X02', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X03', 'DMZ', 'FO', 'PR' )	: '192.168.12.97',
        ( 'X04', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X05', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X06', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X07', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.97',
        ( 'X08', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X09', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X10', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X11', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X12', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X13', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X14', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.98',
        ( 'X15', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X16', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X17', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X18', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X19', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X20', 'DMZ', 'FO', 'PR' ) 	: '192.168.12.99',
        ( 'X01', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X02', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X03', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X04', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X05', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X06', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X07', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.97',
        ( 'X08', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X09', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X10', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X11', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X12', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X13', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X14', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.98',
        ( 'X15', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X16', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X17', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X18', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X19', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X20', 'DMZ', 'BO', 'PR' ) 	: '192.168.12.99',
        ( 'X01', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X02', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X03', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X04', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X04', 'VILLE', '0001', 'R7' ): '10.161.113.60',
        ( 'X05', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X06', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X07', 'DMZ', '0001', 'PR' ) 	: '192.168.12.97',
        ( 'X08', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X09', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X10', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X11', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X12', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X13', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X14', 'DMZ', '0001', 'PR' ) 	: '192.168.12.98',
        ( 'X15', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X16', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X17', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X18', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X19', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X20', 'DMZ', '0001', 'PR' ) 	: '192.168.12.99',
        ( 'X01', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X02', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X03', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X04', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X04', 'VILLE', '0002', 'R7' ): '10.161.113.60',
        ( 'X05', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X06', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X07', 'DMZ', '0002', 'PR' ) 	: '192.168.12.97',
        ( 'X08', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X09', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X10', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X11', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X12', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X13', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X14', 'DMZ', '0002', 'PR' ) 	: '192.168.12.98',
        ( 'X15', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
        ( 'X16', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
        ( 'X17', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
        ( 'X18', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
        ( 'X19', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
        ( 'X20', 'DMZ', '0002', 'PR' ) 	: '192.168.12.99',
    }

    d_appcomp_dir_2_ftpconf = {
        ( 'TOMCAT', 'RO' )		: '''guest_username=%s
local_root=%s
virtual_use_local_privs=YES
write_enable=%s
ascii_download_enable=NO
ascii_upload_enable=NO''',
        ( 'TOMCAT', 'INSTALLER' )	: '''guest_username=%s
local_root=%s
virtual_use_local_privs=YES
write_enable=%s
ascii_download_enable=NO
ascii_upload_enable=NO''',
       ( 'TOMCAT', 'DATAS' )		: '''guest_username=%s
local_root=%s
virtual_use_local_privs=YES
write_enable=%s
ascii_download_enable=NO
ascii_upload_enable=NO''',
       ( 'MYSQL', 'EXECUTABLES' )	: '''guest_username=%s
local_root=%s
virtual_use_local_privs=YES
write_enable=%s
ascii_download_enable=NO
ascii_upload_enable=NO''',
       ( 'MYSQL', 'DUMPS' )		: '''guest_username=%s
local_root=%s
virtual_use_local_privs=YES
write_enable=%s
ascii_download_enable=NO
ascii_upload_enable=NO''',
    }

    d_num_component_2_id_in_username = {
        '0001'      : 'fo',
        '0002'      : 'bo',
        'FO'        : 'fo',
        'BO'        : 'bo',
    }

    d_appcomp_2_appcomp_in_username = {
        'TOMCAT'    : 'tomcat',
        'MYSQL'     : 'mysql',
    }

    d_num_component_2_id_in_username = {
        '0001'      : 'fo',
        '0002'      : 'bo',
        'FO'        : 'pr',
        'BO'        : 'pp',
    }

    d_appcomp_2_paths = {
        ( 'TOMCAT', 'RO', '0001' )     		: '/home/%s/produits/apache-tomcat-6.0.33/webapps/',
        ( 'TOMCAT', 'RO', '0002' )     		: '/home/%s/produits/apache-tomcat-6.0.33/webapps/',
        ( 'TOMCAT', 'RO', 'BO' )     		: '/home/%s/bin/apache-tomcat-5.5.12/webapps/',
        ( 'TOMCAT', 'RO', 'FO' )     		: '/home/%s/bin/apache-tomcat-5.5.12/webapps/',
        ( 'TOMCAT', 'INSTALLER', '0001' )     	: '/home/%s/installer/',
        ( 'TOMCAT', 'INSTALLER', '0002' )     	: '/home/%s/installer/',
        ( 'TOMCAT', 'DATAS', '0001' )     	: '/home/%s/webapp_datas/',
        ( 'TOMCAT', 'DATAS', '0002' )     	: '/home/%s/webapp_datas/',
        ( 'MYSQL', 'DUMPS', '0001' )     	: '/home/%s/dumps/',
        ( 'MYSQL', 'DUMPS', '0002' )     	: '/home/%s/dumps/',
        ( 'MYSQL', 'DUMPS', 'BO' )     		: '/home/%s/dumps/',
        ( 'MYSQL', 'DUMPS', 'FO' )     		: '/home/%s/dumps/',
        ( 'MYSQL', 'EXECUTABLES', '0001' )     	: '/home/%s/executables/',
        ( 'MYSQL', 'EXECUTABLES', '0002' )     	: '/home/%s/executables/',
    }

    d_dir_2_ftp_write = {
        ( 'TOMCAT', 'RO' )		: 'NO',
        ( 'TOMCAT', 'INSTALLER' )	: 'YES',
        ( 'TOMCAT', 'DATAS' )		: 'YES',
        ( 'MYSQL', 'DUMPS' )		: 'NO',
        ( 'MYSQL', 'EXECUTABLES' )	: 'NO',
    }

    def get_ftp_infos( appcode, appcomp, num_component, dir ):

        guest_username 	= '%s_%s_%s' % ( appcode.lower(), d_num_component_2_id_in_username[ num_component ], d_appcomp_2_appcomp_in_username[ appcomp ] )

        local_root 	= d_appcomp_2_paths[ ( appcomp, dir, num_component ) ] % ( guest_username ) 

        write_enable    = d_dir_2_ftp_write[ ( appcomp, dir ) ]

        return (
                   guest_username,
                   local_root,
                   write_enable
               )

    d_ip_2_login_password = {}

    for appcode in sorted( d_appcode_to_aera.keys() ):

        for aera in sorted( d_appcode_to_aera[ appcode ] ):

            for env in sorted( d_appcode_aera_to_env[ ( appcode, aera ) ] ):

                for appcomp in set( sorted( [ k[ 0 ] for k in d_appcomp_num_component_to_dir.keys() ] ) ): 

                    for num_component in set( sorted( [ k[ 1 ] for k in d_appcomp_num_component_to_dir.keys() if ( env, aera, k[ 1 ] ) in d_appcode_2_env_aera_num_comp[ appcode ] ] ) ):

                        for dir in sorted( d_appcomp_num_component_to_dir[ ( appcomp, num_component ) ] ):

                            login 		= '%s_%s_%s_%s' % ( appcode, num_component, appcomp, dir )
    
                            password 		= ''.join([random.choice(letters) for _ in range(8)])
    
                            remote_server	= '%s-%s-%s-%s-%s' % ( appcode, env, appcomp, num_component, aera )
    
                            d.setdefault( appcode, {} ).setdefault( aera, {} ).setdefault( env, {} ).setdefault( appcomp, {} ).setdefault( num_component, {} ).setdefault( dir, {
                                    'os_from_remote_LOGIN'	: login,
                                    'os_from_remote_PASSWORD'	: password,
                                    'os_from_remote_ROOT'	: '/',
                                    'os_from_remote_SERVER'    	: remote_server,
                                }

                            )

                            guest_user_name, local_root, write_enable = get_ftp_infos( appcode, appcomp, num_component, dir )

                            virtual_ftp_user_by_ip_path = virtual_map_ftpusers_dir + d_appcode_aera_num_component_env_2_ip[ ( appcode, aera, num_component, env ) ]


                            if not os.path.isdir( virtual_ftp_user_by_ip_path ):
                                os.mkdir( virtual_ftp_user_by_ip_path )

                            f_virtual_ftp_user = open( virtual_ftp_user_by_ip_path + os.sep + login, 'w' )

                            f_virtual_ftp_user.write( 
                                d_appcomp_dir_2_ftpconf[ ( appcomp, dir ) ] % (
                                    guest_user_name,
                                    local_root,
                                    write_enable,
                                )
                            )
                            f_virtual_ftp_user.close()


                            d_ip_2_login_password.setdefault( d_appcode_aera_num_component_env_2_ip[ ( appcode, aera, num_component, env ) ], '' )
                            d_ip_2_login_password[ d_appcode_aera_num_component_env_2_ip[ ( appcode, aera, num_component, env ) ] ] += '%s\n%s\n' % ( login, password )

                        partial_hosts += '%s\t\t%s\n' % ( d_appcode_aera_num_component_env_2_ip[ ( appcode, aera, num_component, env ) ], remote_server )


    f_virtual_map_json_filepath = open( virtual_map_json_filepath, 'w' )
    json.dump( d, f_virtual_map_json_filepath, sort_keys=True, indent=4)
    f_virtual_map_json_filepath.close()

    for ip, resolv in d_ip_2_login_password.items():
        f_virtual_map_login_password = open( '%s.%s' % ( virtual_map_login_password, ip ), 'w' ) 
        f_virtual_map_login_password.write( resolv )
        f_virtual_map_login_password.close() 

    f_virtual_map_partial_hosts = open( virtual_map_partial_hosts, 'w' )
    f_virtual_map_partial_hosts.write( partial_hosts )
    f_virtual_map_partial_hosts.close()


if __name__ == '__main__':
    main()
