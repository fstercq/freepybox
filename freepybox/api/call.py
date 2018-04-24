class Call:

    def __init__(self, access):
        self._access = access

    async def get_call_list(self):
        '''
        Returns the collection of all call entries
        '''
        return await self._access.get('call/log/')
