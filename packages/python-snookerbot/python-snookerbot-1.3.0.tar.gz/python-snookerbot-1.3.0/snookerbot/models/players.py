from .base import BaseModel, ObjectListModel

class PlayerList(ObjectListModel):

    def __init__(self):
        super().__init__(list_object=Player)

class Player(BaseModel):

    def __init__(self,
        ID=None,
        Type=None,
        FirstName=None,
        LastName=None,
        TeamName=None,
        TeamNumber=None,
        TeamSeason=None,
        ShortName=None,
        Nationality=None,
        Sex=None,
        BioPage=None,
        Born=None,
        Twitter=None,
        SurnameFirst=None,
        License=None,
        Club=None,
        URL=None,
        Photo=None,
        PhotoSource=None,
        FirstSeasonAsPro=None,
        LastSeasonAsPro=None,
        Info=None,
        NumRankingTitles=None,
        NumMaximums=None,
        Died=None
    ):

        super().__init__()

        self.ID = ID
        self.Type = Type
        self.FirstName = FirstName
        self.LastName = LastName
        self.TeamName = TeamName
        self.TeamNumber = TeamNumber
        self.TeamSeason = TeamSeason
        self.ShortName = ShortName
        self.Nationality = Nationality
        self.Sex = Sex
        self.BioPage = BioPage
        self.Born = Born
        self.Twitter = Twitter
        self.SurnameFirst = SurnameFirst
        self.License = License
        self.Club = Club
        self.URL = URL
        self.Photo = Photo
        self.PhotoSource = PhotoSource
        self.FirstSeasonAsPro = FirstSeasonAsPro
        self.LastSeasonAsPro = LastSeasonAsPro
        self.Info = Info
        self.NumRankingTitles = NumRankingTitles
        self.NumMaximums = NumMaximums
        self.Died = Died
        