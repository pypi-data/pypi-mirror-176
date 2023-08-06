from curses import typeahead
from dateutil import parser

class BaseModel:
    
    def __init__(self):

        self.has_error = False
        self.error = None

    def parse(self, json):
        for key, value in json.items():
            lower_key = ''.join(e.lower() for e in key if e.isalnum())
            lower_attrs = { k.replace('_', '').lower() : k for k in self.__dict__.keys() }

            if lower_key in lower_attrs.keys():
                key = lower_attrs[lower_key]

                try:
                    attr_val = getattr(self, key)

                    if isinstance(attr_val, BaseModel):
                        setattr(self, key, attr_val.parse(value))
                    else:

                        # Low effort checking
                        # If the returned key has "Date" in it, we must parse it to a datetime object
                        if('date' in lower_key):
                            try:
                                value = parser.isoparse(value)
                                setattr(self, key, value)
                            except (parser.ParserError, TypeError):
                                pass
                        elif (type(value) == str and value != '') or (type(value) == int and value != 0):
                            setattr(self, key, value)

                except AttributeError:
                    pass

        return self
    
    def get_JSON(self):

        dikt = {}
        for k, v in self.__dict__.items():
            if v:
                if isinstance(v, BaseModel):
                    json = v.get_JSON()
                    if json: dikt[k] = json
                else:
                    dikt[k] = v

        return dikt if len(dikt) > 0 else None
    
    def parse_error(self, json):

        from .errors import Error
        
        self.has_error = True
        self.error = Error().parse(json)

        return self

class ObjectListModel(BaseModel):

    def __init__(self, list=None, list_object=None):
        super().__init__()

        self.list = list if list else []
        self.list_object = list_object
    
    def add(self, item):
        self.list.append(item)
        return self.list
    
    def remove(self, item):
        self.list.remove(item)
        return self.list
    
    def parse(self, json):

        if isinstance(json, dict):
            itemObj = self.list_object().parse(json)
            self.add(itemObj)
        elif isinstance(json, list):
            for item in json:
                itemObj = self.list_object().parse(item)
                self.add(itemObj)

        return self
    
    def get_JSON(self):
        list = []

        for item in self.list:
            list.append(item.get_JSON())
        
        return list if len(list) > 0 else None

    def items(self):
        return self.list