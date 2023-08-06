from urllib3 import PoolManager
from ujson import loads, dumps
from urllib.request import urlopen
from random import choice
from ..encryption import Encryption


class Requests(object):
    def __init__(self, auth: str) -> None:
        self.pm = PoolManager()
        self.auth = auth
        self.web: dict = {'app_name': 'Main', 'app_version': '4.1.7', 'platform': 'Web', 'package': 'web.rubika.ir', 'lang_code': 'fa' }
        self.android: dict = {'app_name': 'Main', 'app_version': '3.0.7', 'platform': 'Android', 'package': 'ir.resaneh1.iptv', 'lang_code': 'fa' }
        self.__address: list = list(loads(urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('API').values())
        self.enc = Encryption(auth)

    async def post(self, url, json=None, is_upload=False, headers=None, data=None):
        if is_upload:
            response = self.pm.request('POST', url, body=data, headers=headers)
            if response.status == 200:
                return loads(response.data.decode('utf-8'))
            return False
        else:
            response = self.pm.request('POST', url, body=dumps(json).encode(), headers={'Content-Type': 'application/json'})
            if response.status == 200:
                return loads(response.data.decode('utf-8'))
            return False

    async def uploadFile(self, url: str, access_hash_send: str, file_id: str, byte: bytes):
        file_size: int = len(byte)
        if file_size <= 131072:
            header: dict = {
				'access-hash-send': access_hash_send,
				'file-id': file_id,
				'part-number': '1',
				'total-part': '1',
				'chunk-size': str(file_size),
				'auth': self.auth
			}
            while True:
                try:
                    result = await self.post(url, data=byte, headers=header)
                    if result: return result
                    else: continue
                except ConnectionError: continue

    async def send(self, method, data, method_type=None, custum_client=False) -> dict:
        if method_type == None:
            data: dict = {'api_version': '4', 'auth': self.auth, 'client': self.android, 'method': method, 'data_enc': self.enc.encrypt(dumps(data))}
            while True:
                try:
                    response = await self.post(self.getDC(), json=data)
                    if response:
                        if response.get('status') == 'OK' and response.get('status_det') == 'OK':
                            response = loads(self.enc.decrypt(response.get('data_enc')))
                            return response
                    else: continue
                except ConnectionError: continue

        elif method_type == 5:
            data: dict = {'api_version': '5', 'auth': self.auth, 'data_enc': self.enc.encrypt(dumps({'method': method, 'input': data, 'client': self.web if custum_client == False else self.android}))}
            while True:
                try:
                    response = await self.post(self.getDC(), json=data)
                    if response:
                        response = loads(self.enc.decrypt(response.get('data_enc')))
                        if response.get('status') == 'OK' and response.get('status_det') == 'OK':
                            repeat = response.get('data').get('status')
                            if repeat == 'Repeated':
                                return 'This Group has timer'
                            else:
                                return response
                    else: continue
                except ConnectionError: continue
    
    def getDC(self) -> str:
        return choice(self.__address)