import requests
import hmac
import time
import json
import ipaddress
import os
import socket
from urllib.parse import urljoin
import freepybox
from freepybox.exceptions import *
from freepybox.access import Access
from freepybox.api.system import System
from freepybox.api.dhcp import Dhcp
from freepybox.api.switch import Switch
from freepybox.api.lan import Lan
from freepybox.api.wifi import Wifi
from freepybox.api.fs import Fs
from freepybox.api.fsnav import Fsnav
from freepybox.api.call import Call


# Token file default location
token_filename = 'app_auth'
token_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(token_dir, token_filename)

# Default application descriptor
app_desc = {
    'app_id':'fpbx',
    'app_name':'freepybox',
    'app_version':freepybox.__version__,
    'device_name':socket.gethostname()
    }


class Freepybox:
    def __init__(self, app_desc=app_desc, token_file=token_file, api_version='v3', timeout=10):
        self.token_file = token_file
        self.api_version = api_version
        self.timeout = timeout
        self.app_desc = app_desc

    def open(self, host, port):
        '''
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules
        '''
        if not self._is_app_desc_valid(self.app_desc): raise InvalidTokenError('invalid application descriptor')

        self.session = requests.Session()
        self.session.verify = os.path.join(os.path.dirname(__file__), 'freebox_root_ca.pem')

        self._access = self._get_freebox_access(host, port, self.api_version, self.token_file, self.app_desc, self.timeout)

        # Instantiate freebox modules
        self.system = System(self._access)
        self.dhcp = Dhcp(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.wifi = Wifi(self._access)
        self.fs = Fs(self._access)
        self.call = Call(self._access)
        self.fsnav = Fsnav(self._access)


    def close(self):
        '''
        Close the freebox session
        '''
        if self._access is None: raise NotOpenError('Freebox is Not opened')

        self._access.post('login/logout')


    def _get_freebox_access(self, host, port, api_version, token_file, app_desc, timeout=10):
        '''
        Returns an access object used for HTTP requests.
        '''

        base_url = self._get_base_url(host, port, api_version)
                
        # Read stored application token
        print('Read application authorization file')
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)
        
        # If no valid token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
                print('No valid authorization file found')
                
                # Get application token from the freebox
                app_token, track_id = self._get_app_token(base_url, app_desc, timeout)
                
                # Check the authorization status
                out_msg_flag = False
                status = None
                while(status != 'granted'):
                    status = self._get_authorization_status(base_url, track_id, timeout)

                    # denied status = authorization failed
                    if status == 'denied':
                        raise AuthorizationError('the app_token is invalid or has been revoked')

                    # Pending status : user must accept the app request on the freebox
                    elif status == 'pending':
                        if not out_msg_flag:
                            out_msg_flag = True
                            print('Please confirm the authentification on the freebox')
                        time.sleep(1)

                    # timeout = authorization failed
                    elif status == 'timeout':
                        raise AuthorizationError('timeout')
                        
                print('Application authorization granted')
                
                # Store application token in file
                self._writefile_app_token(app_token, track_id, app_desc, token_file)
                print('Application token file was generated : {0}'.format(token_file))
        

        # Get token for the current session
        session_token, session_permissions = self._get_session_token(base_url, app_token, app_desc['app_id'], timeout)

        print('Session opened')
        print('Permissions:')
        for i in session_permissions:
            print('{:15s} {:16s}'.format(i, str(session_permissions[i])))


        # Create freebox http access module
        fbx_access = Access(self.session, base_url, session_token, timeout)

        return fbx_access


    def _get_authorization_status(self, base_url, track_id, timeout):
        '''
        Get authorization status of the application token
        Returns:
            unknown 	the app_token is invalid or has been revoked
            pending 	the user has not confirmed the authorization request yet
            timeout 	the user did not confirmed the authorization within the given time
            granted 	the app_token is valid and can be used to open a session
            denied 	    the user denied the authorization request
        '''
        url = urljoin(base_url, 'login/authorize/{0}'.format(track_id))
        r = self.session.get(url, timeout=timeout)
        resp = r.json()
        return resp['result']['status']


    def _get_app_token(self, base_url, app_desc, timeout=10):
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        # Get authentification token
        url = urljoin(base_url, 'login/authorize/')
        data = json.dumps(app_desc)
        r = self.session.post(url, data, timeout=timeout)
        resp = r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('authentification failed')

        app_token = resp['result']['app_token']
        track_id = resp['result']['track_id']

        return(app_token, track_id)


    def _writefile_app_token(self, app_token, track_id, app_desc, file):
        """
        Store the application token in g_app_auth_file file
        """
        d = app_desc
        d.update({'app_token': app_token, 'track_id': track_id})

        with open(file, 'w') as f:
            json.dump(d, f)


    def _readfile_app_token(self, file):
        """
        Read the application token in g_app_auth_file file.
        Returns (app_token, track_id, app_desc)
        """
        try:
            with open(file, 'r') as f:
                d = json.load(f)
                app_token = d['app_token']
                track_id = d['track_id']
                app_desc = {k: d[k] for k in ('app_id', 'app_name', 'app_version', 'device_name') if k in d}
                return (app_token, track_id, app_desc)

        except FileNotFoundError:
            return (None, None, None)


    def _get_session_token(self, base_url, app_token, app_id, timeout=10):
        """
        Get session token from freebox.
        Returns (session_token, session_permissions)
        """
        # Get challenge from API
        challenge = self._get_challenge(base_url, timeout)

        # Hash app_token with chalenge key to get the password
        h = hmac.new(app_token.encode(), challenge.encode(), 'sha1')
        password = h.hexdigest()

        url = urljoin(base_url, 'login/session/')
        data = json.dumps({'app_id': app_id, 'password': password})
        r = self.session.post(url, data, timeout=timeout)
        resp = r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('get_session_token failed')

        session_token = resp.get('result').get('session_token')
        session_permissions = resp.get('result').get('permissions')

        return(session_token, session_permissions)


    def _get_challenge(self, base_url, timeout=10):
        '''
        Return challenge from freebox API
        '''
        url = urljoin(base_url, 'login')
        r = self.session.get(url, timeout=timeout)
        resp = r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('get_challenge failed')

        return resp['result']['challenge']


    def _get_base_url(self, host, port, freebox_api_version):
        '''
        Returns base url for HTTPS requests
        :return:
        '''
        return 'https://{0}:{1}/api/{2}/'.format(host, port, freebox_api_version)


    def _is_app_desc_valid(self, app_desc):
        '''
        Check validity of the application descriptor
        '''
        if all(k in app_desc for k in ('app_id', 'app_name', 'app_version', 'device_name')):
            return True
        else:
            return False
