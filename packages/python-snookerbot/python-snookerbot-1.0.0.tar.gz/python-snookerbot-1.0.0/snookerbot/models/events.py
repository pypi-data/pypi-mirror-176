from dateutil import parser
from .base import BaseModel, ObjectListModel

class EventList(ObjectListModel):

    def __init__(self):
        super().__init__(list_object=Event)

class Event(BaseModel):

    def __init__(self,
        ID=None,
        Name=None,
        StartDate=None,
        EndDate=None,
        Sponsor=None,
        Season=None,
        Type=None,
        Num=None,
        Venue=None,
        City=None,
        Country=None,
        Discipline=None,
        Main=None,
        Sex=None,
        AgeGroup=None,
        Url=None,
        Related=None,
        Stage=None,
        ValueType=None,
        ShortName=None,
        WorldSnookerId=None,
        RankingType=None,
        EventPredictionID=None,
        Team=None,
        Format=None,
        Twitter=None,
        HashTag=None,
        ConversionRate=None,
        AllRoundsAdded=None,
        PhotoURLs=None,
        NumCompetitors=None,
        NumUpcoming=None,
        NumActive=None,
        NumResults=None,
        Note=None,
        CommonNote=None,
        DefendingChampion=None,
        PreviousEdition=None,
        Tour=None
    ):

        super().__init__()

        self.ID = ID
        self.Name = Name
        self.StartDate = parser.parse(StartDate) if StartDate else None
        self.EndDate = parser.parse(EndDate) if EndDate else None
        self.Sponsor = Sponsor
        self.Season = Season
        self.Type = Type
        self.Num = Num
        self.Venue = Venue
        self.City = City
        self.Country = Country
        self.Discipline = Discipline
        self.Main = Main
        self.Sex = Sex
        self.AgeGroup = AgeGroup
        self.Url = Url
        self.Related = Related
        self.Stage = Stage
        self.ValueType = ValueType
        self.ShortName = ShortName
        self.WorldSnookerId = WorldSnookerId
        self.RankingType = RankingType
        self.EventPredictionID = EventPredictionID
        self.Team = Team
        self.Format = Format
        self.Twitter = Twitter
        self.HashTag = HashTag
        self.ConversionRate = ConversionRate
        self.AllRoundsAdded = AllRoundsAdded
        self.PhotoURLs = PhotoURLs
        self.NumCompetitors = NumCompetitors
        self.NumUpcoming = NumUpcoming
        self.NumActive = NumActive
        self.NumResults = NumResults
        self.Note = Note
        self.CommonNote = CommonNote
        self.DefendingChampion = DefendingChampion
        self.PreviousEdition = PreviousEdition
        self.Tour = Tour