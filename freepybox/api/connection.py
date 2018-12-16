class Connection:

    def __init__(self, access):
        self._access = access


    def get_status(self):
        '''
        Get Switch status
        '''
        return self._access.get('connection')

    def get_status_details(self):
        '''
        Get Switch status
        '''
        return self._access.get('connection/full')

    def get_logs(self):
        '''
        Get Switch status
        '''
        return self._access.get('connection/logs')
