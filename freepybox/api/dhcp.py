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
        return self._access.put('dhcp/config/', conf)


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

    def set_static_dhcp_lease(self, data):
        '''
        Add a DHCP static lease
        '''
        return self._access.post('dhcp/static_lease/', payload=data)

    def delete_static_dhcp_lease(self, id):
        '''
        Delete a DHCP static lease with this id
        '''
        return self._access.delete('dhcp/static_lease/{0}'.format(id))


