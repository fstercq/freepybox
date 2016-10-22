class Call:

    def __init__(self, access):
        self._access = access


    def get_call_list(self):
        '''
        Returns the collection of all call entries
        '''
        return self._access.get('call/log/')

