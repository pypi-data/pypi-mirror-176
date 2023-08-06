from .base import APIEndpoint

from snookerbot.models.matches import Match, MatchList

class MatchMethods(APIEndpoint):

    def __init__(self, api):
        super().__init__(api, "")

    def get_ongoing(self):
        url = '?t=7'

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches
    
    def get_upcoming(self):
        url = '?t=14'

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches
    
    def get_event(self, event):
        url = '?t=6&e={event}'.format(event=event)

        status, headers, resp = self.api.get(url)
        if status == 400: return MatchList().parse_error(resp)
        matches = MatchList().parse(resp)
        
        return matches

    def get(self, event_id, round_id, match_number):
        url = '?e={event_id}&r={round_id}&n={match_number}'.format(
            event_id=event_id,
            round_id=round_id,
            match_number=match_number
        )

        status, headers, resp = self.api.get(url)
        if status == 400: return Match().parse_error(resp)
        match = Match().parse(resp[0])

        return match