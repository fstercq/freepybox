class Dhcp:

    def __init__(self, access):
        self._access = access

    async def get_config(self):
        '''
        Get DHCP configuration
        '''
        return await self._access.get('dhcp/config/')

    async def set_config(self, conf):
        '''
        Update a config with new conf dictionary
        '''
        self._access.put('dhcp/config/', conf)

    async def get_dynamic_dhcp_lease(self):
        '''
        Get the list of DHCP dynamic leases
        '''
        return await self._access.get('dhcp/dynamic_lease/')

    async def get_static_dhcp_lease(self):
        '''
        Get the list of DHCP static leases
        '''
        return await self._access.get('dhcp/static_lease/')
