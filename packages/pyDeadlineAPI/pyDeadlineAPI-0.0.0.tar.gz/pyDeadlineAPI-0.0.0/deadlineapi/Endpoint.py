

from deadlineapi.DeadlineObject import DeadlineObj
from deadlineapi.Validation import _is_api_version
from deadlineapi.Validation import _is_url

class Endpoint():
    def __init__(self,jsonobj,endpointname=None,endpointurl=None,ignoreValidationErrors=False) -> None:

        self.endpointname = endpointname
        self.endpointurl = endpointurl

        if 'api' in jsonobj:
            _is_api_version(jsonobj['api'])
            self.api = jsonobj['api']
        else:
            raise Exception("api field is mandatory but not present!")
        
        self.api_compatibility = []
        if 'api_compatibility' in jsonobj:
            for i in jsonobj['api_compatibility']:
                _is_api_version(jsonobj['api'])
                self.api_compatibility.append(i)

        if 'name' in jsonobj:
            self.name = jsonobj['name']
        else:
            raise Exception("name field is mandatory but not present!")

        if 'url' in jsonobj:
            try:
                _is_url(jsonobj['url'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e

            self.url = jsonobj['url']
        else:
            self.url = None

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

        self.deadlines = []
        if 'deadlines' in jsonobj:
            for i in jsonobj['deadlines']:
                self.deadlines.append(DeadlineObj(i,ignoreValidationErrors))