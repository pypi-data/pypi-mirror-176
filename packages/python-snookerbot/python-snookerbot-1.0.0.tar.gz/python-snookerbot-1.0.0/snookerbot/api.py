import requests
import json

from config import BASE_URL

from endpoints.players import PlayerMethods
from endpoints.matches import MatchMethods
from endpoints.events import EventMethods

class SnookerOrgAPI:

    def __init__(self, requested_by):

        self.requested_by = requested_by

        self.headers = {
            'Accept' : 'application/json',
            'Content-Type' : 'application/json',
            'X-Requested-By' : self.requested_by
        }

        self.base_url = BASE_URL

        self.players = PlayerMethods(self)
        self.matches = MatchMethods(self)
        self.events = EventMethods(self)

    def do_request(self, method, url, data=None, headers=None, files=None):

        if headers:
            merged_headers = self.headers
            merged_headers.update(headers)
            headers = merged_headers
        else: headers = self.headers

        req_url = '{base}/{url}'.format(base=self.base_url, url=url)

        if method == 'GET':
            response = requests.get(req_url, params=data, headers=headers, verify=False)
        elif method == 'POST':
            if files: response = requests.post(req_url, data=json.dumps(data), files=files, headers=headers, verify=False)
            else: response = requests.post(req_url, data=json.dumps(data), headers=headers, verify=False)
        elif method == 'PUT':
            response = requests.put(req_url, data=json.dumps(data), headers=headers, verify=False)
        elif method == 'DELETE':
            response = requests.delete(req_url, params=json.dumps(data), headers=headers, verify=False)

        return response

    def request(self, method, url, data=None, headers=None, files=None):
        response = self.do_request(method, url, data, headers, files)
        resp_content = json.loads(response.content) if response.content else None

        return response.status_code, response.headers, resp_content

    def get(self, url, data=None, headers=None):
        status, headers, response = self.request('GET', url, data, headers)
        return status, headers, response
    
    def post(self, url, data=None, headers=None, files=None):
        status, headers, response = self.request('POST', url, data, headers, files)
        return status, headers, response
    
    def put(self, url, data=None, headers=None):
        status, headers, response = self.request('PUT', url, data, headers)
        return status, headers, response
    
    def delete(self, url, data=None, headers=None):
        status, headers, response = self.request('DELETE', url, data, headers)
        return status, headers, response