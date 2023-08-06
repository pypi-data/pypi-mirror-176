from .base import BaseModel, ObjectListModel

class RoundList(ObjectListModel):

    def __init__(self):
        super().__init__(list_object=Round)

class Round(BaseModel):

    def __init__(self,
        Round=None,
        RoundName=None,
        EventID=None,
        MainEvent=None,
        Distance=None,
        NumLeft=None,
        NumMatches=None,
        Note=None,
        ValueType=None,
        Rank=None,
        Money=None,
        SeedGetsHalf=None,
        ActualMoney=None,
        Currency=None,
        ConversionRate=None,
        Points=None,
        SeedPoints=None
    ):

        super().__init__()

        self.Round = Round
        self.RoundName = RoundName
        self.EventID = EventID
        self.MainEvent = MainEvent
        self.Distance = Distance
        self.NumLeft = NumLeft
        self.NumMatches = NumMatches
        self.Note = Note
        self.ValueType = ValueType
        self.Rank = Rank
        self.Money = Money
        self.SeedGetsHalf = SeedGetsHalf
        self.ActualMoney = ActualMoney
        self.Currency = Currency
        self.ConversionRate = ConversionRate
        self.Points = Points
        self.SeedPoints = SeedPoints
                