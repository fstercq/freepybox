class System:

    def __init__(self, access):
        self._access = access


    def get_config(self):
        '''
        Get system configuration:
        '''
        return self._access.get('system/')


    def reboot(self):
        '''
        Reboot freebox
        '''
        self._access.post('system/reboot')




