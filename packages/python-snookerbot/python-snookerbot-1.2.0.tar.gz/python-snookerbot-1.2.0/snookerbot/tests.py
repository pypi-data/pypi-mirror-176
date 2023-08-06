import api

snooker_api = api.SnookerOrgAPI('alexander.schillemans@hotmail.com')

# mark_williams = snooker_api.players.get(1)

# print(mark_williams.FirstSeasonAsPro)
# print(mark_williams.LastSeasonAsPro)

# matches = snooker_api.matches.get_event(398)

# for match in matches.items():
#     print(match.ID)

events = snooker_api.events.get_in_season(2022)
for event in events.items():
    print(event.Name)
    date = event.StartDate.strftime('%d/%m/%Y')
    print(date)