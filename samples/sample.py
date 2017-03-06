# -*- coding: utf-8 -*-

"""Rancidcmd sample."""

from rancidcmd import RancidCmd


def main():
    """Sample main."""

    #################################################
    # Rancid path ###################################
    #################################################

    # for CentOS
    clogin = '/usr/libexec/rancid/clogin'
    jlogin = '/usr/libexec/rancid/jlogin'

    # # for Debian/Ubuntu
    # clogin = '/usr/lib/rancid/bin/clogin'
    # jlogin = '/usr/lib/rancid/bin/jlogin'

    # # for Mac OS X
    # clogin = '/opt/local/libexec/rancid/clogin'
    # jlogin = '/opt/local/libexec/rancid/jlogin'

    #################################################
    # Node Info #####################################
    #################################################

    user = 'user'
    password = 'password'
    enable_password = 'enable password'
    cmd = 'show version'

    nodes = [

        {'name': 'Router1',
         'addr': '192.168.1.1',
         'port': 23,
         'method': 'telnet',
         'cmd': cmd,
         'password': password,
         'enable_password': enable_password,
         'login': clogin},

        {'name': 'Router2',
         'addr': '192.168.1.2',
         'port': 22,
         'method': 'ssh',
         'cmd': cmd,
         'password': password,
         'enable_password': None,
         'login': jlogin},

        {'name': 'Router3',
         'addr': '192.168.1.3',
         'port': 2601,
         'method': 'telnet',
         'cmd': cmd,
         'password': password,
         'enable_password': None,
         'login': clogin},
    ]

    #################################################
    # Run ###########################################
    #################################################

    for node in nodes:

        args = dict(user=user,
                    password=node['password'],
                    enable_password=node['enable_password'],
                    login=node['login'],
                    address=node['addr'],
                    port=node['port'],
                    method=node['method'])

        rancid = RancidCmd(**args)
        res = rancid.execute(node['cmd'])
        if res['rtn_code'] == 0:
            print(res['std_out'])
        else:
            print('[error] %s' % res['std_err'])


if __name__ == "__main__":

    main()
