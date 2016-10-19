from .fs import Fs
import os

class Fsnav:

    def __init__(self, access):
        self._fs = Fs(access)
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
        norm_path = os.path.normpath(path)
        if norm_path == '.':
            pass

        elif norm_path == '..':
            self._path = os.path.dirname(self._path)

        else:
            if self._path_exists(path):
                self._path = os.path.join(self._path, path)
            else:
                print('{0} does not exist'.format(os.path.join(self._path, path)))


    def _path_exists(self, path):
        '''
        Return True if the path exists
        '''
        try:
            self._fs.get_file_info(os.path.join(self._path, path))
            return True
        except:
            return False


    def ls(self):
        '''
        list directory
        '''
        for i in self._fs.list_file(self._path):
            print(i['name'])

