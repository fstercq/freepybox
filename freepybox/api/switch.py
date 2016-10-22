class Switch:

    def __init__(self, access):
        self._access = access


    def get_status(self):
        '''
        Get Switch status
        '''
        return self._access.get('switch/status/')


    def get_port_conf(self, port_id):
        '''
        Get port_id Port configuration
        '''
        return self._access.get('switch/port/{0}'.format(port_id))


    def set_port_conf(self, port_id, conf):
        '''
        Update port_id Port configuration with conf dictionary
        '''
        self._access.put('switch/port/{0}'.format(port_id), conf)


    def get_port_stats(self, port_id):
        '''
        Get port_id Port stats
        '''
        return self._access.get('switch/port/{0}/{1}'.format(port_id, 'stats'))
