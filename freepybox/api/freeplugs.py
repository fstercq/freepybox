class Freeplugs:

    def __init__(self, access):
        self._access = access


    def get_freeplugs_list(self):
        '''
        Get freeplugs list
        '''
        return self._access.get('freeplug/')


    def get_freeplug(self, fp_id):
        '''
        Get freeplug with the specific id
        '''
        return self._access.get('freeplug/{0}/'.format(fp_id))
