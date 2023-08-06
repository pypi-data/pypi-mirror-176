from .base import BaseModel, ObjectListModel

class MatchList(ObjectListModel):

    def __init__(self):
        super().__init__(list_object=Match)

class Match(BaseModel):

    def __init__(self,
        ID=None,
        EventID=None,
        Round=None,
        Number=None,
        Player1ID=None,
        Score1=None,
        Walkover1=None,
        Player2ID=None,
        Score2=None,
        Walkover2=None,
        WinnerID=None,
        Unfinished=None,
        onBreak=None,
        Status=None,
        WorldSnookerID=None,
        LiveUrl=None,
        DetailsUrl=None,
        PointsDropped=None,
        ShowCommonNote=None,
        Estimated=None,
        Type=None,
        TableNo=None,
        VideoURL=None,
        InitDate=None,
        ModDate=None,
        StartDate=None,
        EndDate=None,
        ScheduledDate=None,
        FrameScores=None,
        Sessions=None,
        Note=None,
        ExtendedNote=None
    ):

        super().__init__()

        self.ID = ID
        self.EventID = EventID
        self.Round = Round
        self.Number = Number
        self.Player1ID = Player1ID
        self.Score1 = Score1
        self.Walkover1 = Walkover1
        self.Player2ID = Player2ID
        self.Score2 = Score2
        self.Walkover2 = Walkover2
        self.WinnerID = WinnerID
        self.Unfinished = Unfinished
        self.onBreak = onBreak
        self.Status = Status
        self.WorldSnookerID = WorldSnookerID
        self.LiveUrl = LiveUrl
        self.DetailsUrl = DetailsUrl
        self.PointsDropped = PointsDropped
        self.ShowCommonNote = ShowCommonNote
        self.Estimated = Estimated
        self.Type = Type
        self.TableNo = TableNo
        self.VideoURL = VideoURL
        self.InitDate = InitDate
        self.ModDate = ModDate
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.ScheduledDate = ScheduledDate
        self.FrameScores = FrameScores
        self.Sessions = Sessions
        self.Note = Note
        self.ExtendedNote = ExtendedNote
        