class Fw:

    def __init__(self, access):
        self._access = access

    def get_forward(self):
        '''
        Getting the list of port forwarding
        '''
        return self._access.get('fw/redir/')

    def add_forward(self, data):
        '''
        Add a port forwarding
        '''
        return self._access.post('fw/redir/', payload=data)

    def delete_forward(self, id):
        '''
        Delete a port forwarding
        '''
        return self._access.delete('fw/redir/{0}'.format(id))

