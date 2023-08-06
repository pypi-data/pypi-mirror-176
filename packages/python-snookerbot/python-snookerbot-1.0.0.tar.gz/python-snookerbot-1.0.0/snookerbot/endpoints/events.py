from .base import APIEndpoint

from models.events import Event, EventList
from models.rounds import RoundList, Round

class EventMethods(APIEndpoint):

    def __init__(self, api):
        super().__init__(api, "")

    def get(self, id):
        url = '?e={id}'.format(id=id)

        status, headers, resp = self.api.get(url)
        if status == 400: return Event().parse_error(resp)
        event = Event().parse(resp[0])
        
        return event
    
    def get_in_season(self, season):
        url = '?t=5&s={season}'.format(season=season)

        status, headers, resp = self.api.get(url)
        if status == 400: return EventList().parse_error(resp)
        events = EventList().parse(resp)
        
        return events
    
    def get_rounds(self, id):
        url = '?t=12&e={id}'.format(id=id)

        status, headers, resp = self.api.get(url)
        if status == 400: return RoundList().parse_error(resp)
        rounds = RoundList().parse(resp)
        
        return rounds