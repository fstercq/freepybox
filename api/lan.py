class Lan:

    def __init__(self, access):
        self._access = access


    def get_config(self):
        '''
        Get Lan configuration
        '''
        return self._access.get('lan/config/')


    def set_config(self, conf):
        '''
        Update Lan config with conf dictionary
        '''
        self._access.put('lan/config/', conf)


    def get_interfaces(self):
        '''
        Get browsable Lan interfaces
        '''
        return self._access.get('lan/browser/interfaces')


    def get_hosts_list(self, interface='pub'):
        '''
        Get the list of hosts on a given interface¶
        '''
        return self._access.get('lan/browser/{0}'.format(interface))


    def get_host_information(self, host_id, interface='pub'):
        '''
        Get specific host informations on a given interface¶
        '''
        return self._access.get('lan/browser/{0}/{1}'.format(interface, host_id))


    def set_host_information(self, host_id, conf, interface='pub'):
        '''
        Update specific host informations on a given interface¶
        '''
        self._access.put('lan/browser/{0}/{1}'.format(interface, host_id), conf)



