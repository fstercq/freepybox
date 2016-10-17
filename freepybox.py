import requests
import hmac
import time
import json
import ipaddress
from urllib.parse import urljoin
from .config import *
from .access import Access
from .api.system import System
from .api.dhcp import Dhcp
from .api.switch import Switch
from .api.lan import Lan
from .api.wifi import Wifi


conf_desc = {
    'freebox_api_version': freebox_api_version,
    'app_token_file_path': app_token_file_path,
    'app_id': app_name + app_version,
    'app_name': app_name,
    'app_version': app_version,
    'device_name': dev_name,
    'http_timeout': http_timeout}


class Freepybox:
    def __init__(self, ip, port=80, protocol='http', conf=conf_desc):

        self._ip = ip
        self._base_url = '{0}://{1}:{2}/api/{3}/'.format(protocol, ip, port, conf['freebox_api_version'])
        self._conf = conf

        # Obtain session token from the freebox
        self._session_token, self._session_permission = self._login()

        # Create freebox http access module
        self._access = Access(self._base_url, self._session_token, self._conf['http_timeout'])

        # Instantiate freebox modules
        self.system = System(self._access)
        self.dhcp = Dhcp(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.wifi = Wifi(self._access)


    def close(self):
        '''
        Close the freebox session
        '''
        self._access.post('login/logout')


    def _login(self):
        '''
        Login to the freebox : obtain a session token from the API
        '''

        # Check wether IP is private
        try:
                is_private_ip = ipaddress.ip_address(self._ip).is_private
        except ValueError:
                is_private_ip = False
                
        # Read stored application token
        print('Read application authorization file')
        is_stored_token_valid = self._read_app_token()
        app_token, track_id = is_stored_token_valid if is_stored_token_valid is not False else (None, None)
        
        # If no application token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None:
                print('No authorization file found')
                # Raise Error if not private connection
                if not is_private_ip:
                        raise Exception('No authorization file found for this application. Please connect in LAN to get authorization from the Freebox')
                
                # Get application token from the freebox
                app_token, track_id = self._get_app_token()
                
                # Check the authorization status
                out_msg_flag = False
                status = None
                while(status != 'granted'):
                    status = self._get_authorization_status(track_id)

                    # denied status = authorization failed
                    if status == 'denied':
                        raise Exception('authorization denied : the app_token is invalid or has been revoked')

                    # Pending status : user must accept the app request on the freebox
                    elif status == 'pending':
                        if not out_msg_flag:
                            out_msg_flag = True
                            print('Please confirm the authentification on the freebox')
                        time.sleep(1)

                    # timeout = authorization failed
                    elif status == 'timeout':
                        raise Exception('authorization denied : timeout')
                        
                print('Application authorization granted')
                
                # Store application token in file
                self._write_app_token(app_token, track_id)
                print('Application token file was generated : {0}'.format(self._conf['app_token_file_path']))
        

        # Get token for the current session
        session_token, session_permissions = self._get_session_token(app_token, self._conf['app_id'])

        print('Session opened')
        print('Permissions:')
        for i in session_permissions:
            print('{:15s} {:16s}'.format(i, str(session_permissions[i])))

        return session_token, session_permissions


    def _get_authorization_status(self, track_id):
        '''
        Get authorization status of the application token
        Returns:
            unknown 	the app_token is invalid or has been revoked
            pending 	the user has not confirmed the authorization request yet
            timeout 	the user did not confirmed the authorization within the given time
            granted 	the app_token is valid and can be used to open a session
            denied 	    the user denied the authorization request
        '''
        url = urljoin(self._base_url, 'login/authorize/{0}'.format(track_id))
        r = requests.get(url, timeout=self._conf['http_timeout'])
        resp = r.json()
        return resp['result']['status']


    def _get_app_token(self):
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        # Get authentification token
        url = urljoin(self._base_url, 'login/authorize/')
        payload = {
            'app_id': self._conf['app_name'] + self._conf['app_version'],
            'app_name': self._conf['app_name'],
            'app_version': self._conf['app_version'],
            'device_name': self._conf['device_name']}

        data = json.dumps(payload)
        r = requests.post(url, data=data, timeout=self._conf['http_timeout'])
        resp = r.json()

        # raise exception if resp.success != True
        if resp.get('success') != True:
            raise Exception('authentification failed')

        app_token = resp['result']['app_token']
        track_id = resp['result']['track_id']

        return(app_token, track_id)


    def _write_app_token(self, app_token, track_id):
        """
        Store the application token in g_app_auth_file file
        """
        with open(self._conf['app_token_file_path'], 'w') as f:
            f.write(app_token+'\n')
            f.write(str(track_id))


    def _read_app_token(self):
        """
        Read the application token in g_app_auth_file file.
        Return False if the file doesn't exist else return (app_token, track_id)
        """
        try:
            with open(self._conf['app_token_file_path'], 'r') as f:
                app_token = f.readline().split()[0]
                track_id = f.readline().split()[0]
                return (app_token, track_id)

        except FileNotFoundError:
            return False


    def _get_session_token(self, app_token, app_id):
        """
        Get session token from app_token._get_session_token
        Returns (session_token, session_permissions)
        """
        # Get challenge from API
        challenge = self._get_challenge()

        # Hash app_token with chalenge key to get the password
        h = hmac.new(app_token.encode(), challenge.encode(), 'sha1')
        password = h.hexdigest()

        url = urljoin(self._base_url, 'login/session/')
        data = json.dumps({'app_id': app_id, 'password': password})
        r = requests.post(url, data, timeout=self._conf['http_timeout'])
        resp = r.json()

        # raise exception if resp.success != True
        if resp.get('success') != True:
            raise Exception('get_session_token failed')

        session_token = resp.get('result').get('session_token')
        session_permissions = resp.get('result').get('permissions')

        return(session_token, session_permissions)


    def _get_challenge(self):
        '''
        Return challenge from freebox API
        '''
        url = urljoin(self._base_url, 'login')
        r = requests.get(url, timeout=self._conf['http_timeout'])
        resp = r.json()

        # raise exception if resp.success != True
        if resp.get('success') != True:
            raise Exception('get_challenge failed')

        return resp['result']['challenge']
