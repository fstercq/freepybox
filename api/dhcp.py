class Dhcp:

    def __init__(self, access):
        self._access = access


    def get_config(self):
        '''
        Get DHCP configuration
        '''
        return self._access.get('dhcp/config/')


    def set_config(self, conf):
        '''
        Update a config with new conf dictionary
        '''
        self._access.put('dhcp/config/', conf)


    def get_dynamic_dhcp_lease(self):
        '''
        Get the list of DHCP dynamic leases
        '''
        return self._access.get('dhcp/dynamic_lease/')


    def get_static_dhcp_lease(self):
        '''
        Get the list of DHCP static leases
        '''
        return self._access.get('dhcp/static_lease/')



