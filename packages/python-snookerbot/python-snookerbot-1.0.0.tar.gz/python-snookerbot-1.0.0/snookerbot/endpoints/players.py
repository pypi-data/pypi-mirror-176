from .base import APIEndpoint

from models.players import Player, PlayerList

class PlayerMethods(APIEndpoint):

    def __init__(self, api):
        super().__init__(api, "?p=")

    def get(self, id):
        url = '{endpoint}{id}'.format(endpoint=self.endpoint, id=id)

        status, headers, resp = self.api.get(url)
        if status == 400: return Player().parse_error(resp)
        player = Player().parse(resp[0])
        
        return player