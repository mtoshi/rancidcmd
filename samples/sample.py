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

    # # for Debian
    # clogin = '/usr/lib/rancid/bin/clogin'
    # jlogin = '/usr/lib/rancid/bin/jlogin'

    # # for Mac OS X
    # clogin = '/opt/local/libexec/rancid/bin/clogin'
    # jlogin = '/opt/local/libexec/rancid/bin/jlogin'

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
         'cmd': cmd,
         'password': password,
         'enable_password': enable_password,
         'login': clogin},

        {'name': 'Router2',
         'addr': '192.168.1.2',
         'cmd': cmd,
         'password': password,
         'enable_password': None,
         'login': jlogin},

        {'name': 'Router3',
         'addr': '192.168.1.3',
         'cmd': cmd,
         'password': password,
         'enable_password': None,
         'login': jlogin},
    ]

    #################################################
    # Run ###########################################
    #################################################

    for node in nodes:

        args = dict(user=user,
                    password=node['password'],
                    enable_password=node['enable_password'],
                    login=node['login'],
                    address=node['addr'])

        rancid = RancidCmd(**args)

        res = rancid.execute(node['cmd'])

        if res['rtn_code'] == 0:
            print(res['std_out'])
        else:
            print('[error] %s' % res['std_err'])


if __name__ == "__main__":

    main()
