from .base import APIEndpoint

from models.matches import Match, MatchList

class MatchMethods(APIEndpoint):

    def __init__(self, api):
        super().__init__(api, "?t=")

    def get_ongoing(self):
        url = '{endpoint}7'.format(endpoint=self.endpoint)

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches
    
    def get_upcoming(self):
        url = '{endpoint}14'.format(endpoint=self.endpoint)

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches
    
    def get_event(self, event):
        url = '{endpoint}6&e={event}'.format(endpoint=self.endpoint, event=event)

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches