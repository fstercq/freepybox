class Phone:

    def __init__(self, access):
        self._access = access


    def get_config(self):
        '''
        Get phone configuration:
        '''
        return self._access.get('phone/')


    def set_config(self, conf):
        '''
        Update phone configuration:
        '''
        self._access.put('phone/', conf)


    def get_dect_vendors(self):
        '''
        Get phone configuration:
        '''
        return self._access.get('phone/dect_vendors/')

