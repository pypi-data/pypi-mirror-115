



from deadlineapi.Contact import Contact
from deadlineapi.Location import Location
from deadlineapi.Validation import _is_url, _is_valid_date, _is_valid_deadline

class DeadlineObj():

    def __init__(self,jsonobj,ignoreValidationErrors=False):
        if 'name' in jsonobj:
            self.name = jsonobj['name']
        else:
            raise Exception("name field is mandatory but not present!")

        self.categories = []
        if 'categories' in jsonobj:
            for i in jsonobj['categories']:
                self.categories.append(i)

        if 'location' in jsonobj:
            self.location = Location(jsonobj['location'],ignoreValidationErrors)
        else:
            raise Exception("location field is mandatory but not present!")

        if 'contact' in jsonobj:
            self.contact = Contact(jsonobj['contact'],ignoreValidationErrors)
        else:
            raise Exception("contact field is mandatory but not present!")
        
        if 'startdate' in jsonobj:
            _is_valid_date(jsonobj['startdate'])
            self.startdate = jsonobj['startdate']
        else:
            raise Exception("startdate field is mandatory but not present!")

        if 'deadline' in jsonobj:
            _is_valid_deadline(jsonobj['deadline'])
            self.deadline = jsonobj['deadline']
        else:
            raise Exception("deadline field is mandatory but not present!")

        if 'shortname' in jsonobj:
            self.shortname = jsonobj['shortname']
        else:
            self.shortname = None

        if 'logo' in jsonobj:
            try:
                _is_url(jsonobj['logo'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e

            self.logo = jsonobj['logo']
        else:
            self.logo = None

        if 'cfpurl' in jsonobj:
            try:
                _is_url(jsonobj['cfpurl'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e

            self.cfpurl = jsonobj['cfpurl']
        else:
            self.cfpurl = None

        if 'confurl' in jsonobj:
            try:
                _is_url(jsonobj['confurl'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e

            self.confurl = jsonobj['confurl']
        else:
            self.confurl = None

        if 'enddate' in jsonobj:
            _is_valid_date(jsonobj['enddate'])
            self.enddate = jsonobj['enddate']
        else:
            self.enddate = None

        if 'pagelimit' in jsonobj:
            self.pagelimit = int(jsonobj['pagelimit'])
        else:
            self.pagelimit = None

    def days_left(self) -> int:
        # TODO
        pass

    def hours_left(self) -> int:
        # TODO
        pass

    def minutes_left(self) -> int:
        # TODO
        pass

    def seconds_left(self) -> int:
        # TODO
        pass

    def countdown(self) -> str:
        # TODO
        pass

    def timediff(self):
        # TODO
        pass

