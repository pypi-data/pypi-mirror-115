

class Location():
    def __init__(self,jsonobj,ignoreValidationErrors=False) -> None:

        if 'virtual' in jsonobj:
            self.virtual = jsonobj['virtual']
        else:
            raise Exception("virtual field is mandatory but not present!")

        if 'country' in jsonobj:
            self.country = jsonobj['country']
        elif self.virtual:
            self.country = None
        else:
            raise Exception("country field is mandatory for non-virtual conferences but not present!")

        if 'city' in jsonobj:
            self.city = jsonobj['city']
        elif self.virtual:
            self.city = None
        else:
            raise Exception("city field is mandatory for non-virtual conferences but not present!")

        if 'lat' in jsonobj:
            self.lat = float(jsonobj['lat'])
        else:
            self.lat = None

        if 'lon' in jsonobj:
            self.lon = float(jsonobj['lon'])
        else:
            self.lon = None
        
    def to_str(self) -> str:
        if self.virtual:
            return "Virtual"
        else:
            return f"{self.country}, {self.city}"