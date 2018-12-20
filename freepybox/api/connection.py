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
