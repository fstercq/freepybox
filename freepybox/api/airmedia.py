class Airmedia:

    def __init__(self, access):
        self._access = access


    def get_config(self):
        '''
        Get Airmedia configuration
        '''
        return self._access.get('airmedia/config/')


    def set_config(self, conf):
        '''
        Update Airmedia configuration with conf dictionary
        '''
        self._access.put('airmedia/config/', conf)
