class Switch:

    def __init__(self, access):
        self._access = access

    async def get_status(self):
        '''
        Get Switch status
        '''
        return await self._access.get('switch/status/')

    async def get_port_conf(self, port_id):
        '''
        Get port_id Port configuration
        '''
        return await self._access.get('switch/port/{0}'.format(port_id))

    async def set_port_conf(self, port_id, conf):
        '''
        Update port_id Port configuration with conf dictionary
        '''
        await self._access.put('switch/port/{0}'.format(port_id), conf)

    async def get_port_stats(self, port_id):
        '''
        Get port_id Port stats
        '''
        return await self._access.get('switch/port/{0}/{1}'.format(port_id, 'stats'))
