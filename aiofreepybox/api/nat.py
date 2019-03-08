class Nat:

    def __init__(self, access):
        self._access = access

    async def get_port_forwarding_list(self):
        '''
        Get the list of port forwarding
        '''
        return await self._access.get('fw/redir/')

    async def get_port_forwarding(self, redir_id):
        '''
        Get a specific port forwarding
        '''
        return await self._access.get('fw/redir/{0}'.format(redir_id))

    async def set_port_forwarding(self, redir_id, conf):
        '''
        Update a port forwarding
        '''
        return await self._access.put('fw/redir/{0}'.format(redir_id), conf)

    async def create_port_forwarding(self, conf):
        '''
        Add a port forwarding
        '''
        return await self._access.post('fw/redir/', conf)

    async def delete_port_forwarding(self, redir_id):
        '''
        Delete a port forwarding
        '''
        return await self._access.delete('fw/redir/{0}'.format(redir_id))

    async def get_incoming_port_list(self):
        '''
        Get the list of incoming ports
        '''
        return await self._access.get('fw/incoming/')

    async def get_incoming_port(self, inc_port_id):
        '''
        Get a specific incoming port
        '''
        return await self._access.get('fw/incoming/{}'.format(inc_port_id))

    async def set_incoming_port(self, inc_port_id, conf):
        '''
        Update an incoming port
        '''
        return await self._access.put('fw/incoming/{}'.format(inc_port_id), conf)

    async def get_dmz(self):
        '''
        Get the current DMZ configuration
        '''
        return await self._access.get('fw/dmz/')

    async def set_dmz(self, conf):
        '''
        Update the current DMZ configuration
        '''
        return await self._access.put('fw/dmz/', conf)
