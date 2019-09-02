class Wifi:

    def __init__(self, access):
        self._access = access


    def get_global_config(self):
        '''
        Get wifi global configuration:
        '''
        return self._access.get('wifi/config/')


    def set_global_config(self, conf):
        '''
        Update wifi global configuration:
        '''
        self._access.put('wifi/config/', conf)


    def get_ap_list(self):
        '''
        Get wifi access points list
        '''
        return self._access.get('wifi/ap/')


    def get_ap(self, ap_id):
        '''
        Get wifi access point with the specific id
        '''
        return self._access.get('wifi/ap/{0}'.format(ap_id))


    def set_ap(self, ap_id, conf):
        '''
        Update wifi access point with the specific id
        '''
        self._access.get('wifi/ap/{0}'.format(ap_id), conf)
        

    def get_ap_allowed_channel(self, ap_id):
        '''
        Get allowed channels of the wifi access point
        '''
        return self._access.get('wifi/ap/{0}/allowed_channel_comb/'.format(ap_id))


    def get_station_list(self, ap_id):
        '''
        Get the list of Wifi Stations associated to the AP
        '''
        return self._access.get('wifi/ap/{0}/stations/'.format(ap_id))


    def get_ap_neighbors(self, ap_id):
        '''
        Get the list of Wifi neighbors seen by the AP
        '''
        return self._access.get('wifi/ap/{0}/neighbors/'.format(ap_id))

    def get_bss_list(self):
        '''
        Get wifi BSS list
        '''
        return self._access.get('wifi/bss/')

    def get_bss(self, ap_id):
        '''
        Get wifi BSS with the specific id
        '''
        return self._access.get('wifi/bss/{0}'.format(ap_id))

    def set_bss(self, ap_id, conf):
        '''
        Update wifi BSS with the specific id
        '''
        self._access.get('wifi/bss/{0}'.format(ap_id), conf)
