
from deadlineapi.Loader import load_endpoint_by_url

class DirectoryItem():
    def __init__(self, endpointname, endpointurl):
        self.endpointname = endpointname
        self.endpointurl = endpointurl

    def load(self):
        return load_endpoint_by_url(self.endpointurl,endpointname=self.endpointname,endpointurl=self.endpointurl)