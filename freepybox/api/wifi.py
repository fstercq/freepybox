class Wifi:

    def __init__(self, access):
        self._access = access

    async def get_global_config(self):
        '''
        Get wifi global configuration:
        '''
        return await self._access.get('wifi/config/')


    async def set_global_config(self, conf):
        '''
        Update wifi global configuration:
        '''
        await self._access.put('wifi/config/', conf)

    async def get_ap_list(self):
        '''
        Get wifi access points list
        '''
        return await self._access.get('wifi/ap/')

    async def get_ap(self, ap_id):
        '''
        Get wifi access point with the specific id
        '''
        return await self._access.get('wifi/ap/{0}'.format(ap_id))

    async def set_ap(self, ap_id, conf):
        '''
        Update wifi access point with the specific id
        '''
        await self._access.get('wifi/ap/{0}'.format(ap_id), conf)

    async def get_ap_allowed_channel(self, ap_id):
        '''
        Get allowed channels of the wifi access point
        '''
        return await self._access.get('wifi/ap/{0}/allowed_channel_comb/'.format(ap_id))

    async def get_station_list(self, ap_id):
        '''
        Get the list of Wifi Stations associated to the AP
        '''
        return await self._access.get('wifi/ap/{0}/stations/'.format(ap_id))

    async def get_ap_neighbors(self, ap_id):
        '''
        Get the list of Wifi neighbors seen by the AP
        '''
        return await self._access.get('wifi/ap/{0}/neighbors/'.format(ap_id))
