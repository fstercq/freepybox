import base64
import os
import logging

logger = logging.getLogger(__name__)

class Fs:

    def __init__(self, access):
        self._access = access
        self._path = '/'


    def pwd(self):
        '''
        Print working directory
        '''
        print(self._path)


    def cd(self, path):
        '''
        Change directory
        '''
        if self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            logger.error('{0} does not exist'.format(os.path.join(self._path, path)))


    def _path_exists(self, path):
        '''
        Return True if the path exists
        '''
        try:
            self.get_file_info(os.path.join(self._path, path))
            return True
        except:
            return False


    def ls(self):
        '''
        list directory
        '''
        for i in self.list_file(self._path):
            print(i['name'])


    def get_tasks_list(self):
        '''
        Return the collection of all tasks
        '''
        return self._access.get('fs/tasks/')


    def list_file(self, path):
        '''
        Returns the list of files for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return self._access.get('fs/ls/{0}'.format(path_b64))


    def get_file_info(self, path):
        '''
        Returns informations for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return self._access.get('fs/ls/{0}'.format(path_b64))

