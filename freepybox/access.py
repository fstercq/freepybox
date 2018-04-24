import json
from urllib.parse import urljoin
from freepybox.exceptions import *


class Access:
    def __init__(self, session, base_url, session_token, http_timeout):
        self.session = session
        self.header = {'X-Fbx-App-Auth': session_token}
        self.base_url = base_url
        self.timeout = http_timeout

    async def get(self, end_url):
        '''
        Send get request and return results
        '''
        url = urljoin(self.base_url, end_url)
        r = await self.session.get(url, headers=self.header, timeout=self.timeout)
        resp = await r.json()

        if not resp['success']:
            raise HttpRequestError(resp['error_code'])

        if 'result' in resp:
            return resp['result']

    async def post(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = await self.session.post(url, headers=self.header, data=data, timeout=self.timeout)
        resp = await r.json()

        if not resp['success']:
            raise HttpRequestError(resp['error_code'])

        if 'result' in resp:
            return resp['result']

    async def put(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = await self.session.put(url, headers=self.header, data=data, timeout=self.timeout)
        resp = await r.json()

        if not resp['success']:
            raise HttpRequestError(resp['error_code'])

        if 'result' in resp:
            return resp['result']
