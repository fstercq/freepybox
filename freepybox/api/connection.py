class Connection:

    def __init__(self, access):
        self._access = access


    def get_status(self):
        '''
        Get Connection status
        '''
        return self._access.get('connection')

    def get_status_details(self):
        '''
        Get Connection detailed status
        '''
        return self._access.get('connection/full')

    def get_logs(self):
        '''
        Get Connection logs
        '''
        return self._access.get('connection/logs')

    def get_xdsl_stats(self):
        '''
        Get port_id xDSL stats
        '''
        return self._access.get('connection/xdsl')

    def get_ftth_stats(self):
        '''
        Get the current FTTH status
        '''
        return self._access.get('connection/ftth')


    def get_ipv6_config(self):
        '''
        Get the current IPv6 Connection configuration
        '''
        return self._access.get('connection/ipv6/config')


    def set_ipv6_config(self, conf):
        '''
        SUpdate the IPv6 Connection configuration
        '''
        return self._access.put('connection/ipv6/config', conf)

