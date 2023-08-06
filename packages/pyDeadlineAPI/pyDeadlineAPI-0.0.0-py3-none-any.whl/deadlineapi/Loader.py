

import json
import requests
import os

import deadlineapi.Endpoint
import deadlineapi.DirectoryItem
from deadlineapi.Validation import _is_valid_schema_by_jsonobj,_is_url


# Functions to load endpoints

def load_endpoint_by_json(jsonobj,endpointname=None,endpointurl=None,ignoreValidationErrors=False):
    _is_valid_schema_by_jsonobj(jsonobj)
    return deadlineapi.Endpoint(jsonobj,endpointname=endpointname,endpointurl=endpointurl,ignoreValidationErrors=ignoreValidationErrors)

def load_endpoint_by_string(s,endpointname=None,endpointurl=None,ignoreValidationErrors=False):
    jsonobj = json.loads(s)
    return load_endpoint_by_json(jsonobj)

def load_endpoint_by_path(path,endpointname=None,endpointurl=None,ignoreValidationErrors=False):
    return load_endpoint_by_string(open(path,'r').read())

def load_endpoint_by_url(url,endpointname=None,endpointurl=None,ignoreValidationErrors=False):
    _is_url(url)
    return load_endpoint_by_string(requests.get(url=url,timeout=5).text)


# Functions to load directories

DEFAULT_DIRECTORY_URL = "https://directory.deadlineapi.org/directory.json"

def load_directory_by_string(s,loadDirectly=True,failOnLoadingError=True,ignoreValidationErrors=False):
    directory = json.loads(s)

    if loadDirectly:
        # Directly load Endpoints. This may take some time
        endpoints = []
        for k in directory:
            #print(f"Loading endpoint {k} with url {directory[k]}")
            try:
                endpoints.append(load_endpoint_by_url(directory[k],ignoreValidationErrors))
            except Exception as e:
                if failOnLoadingError:
                    raise Exception(f"Failed to load endpoint {k}: {e}")
        return endpoints
    else:
        # Only create DirectoryItem form the key-value pairs
        items = []
        for k in directory:
            items.append(deadlineapi.DirectoryItem(k,directory[k]))
        return items

def load_directory_by_url(url=DEFAULT_DIRECTORY_URL,loadDirectly=True,failOnLoadingError=False,ignoreValidationErrors=False):
    return load_directory_by_string(requests.get(url=url,timeout=5).text)
    
def load_directory_by_path(path,loadDirectly=True,failOnLoadingError=False,ignoreValidationErrors=False):
    return load_directory_by_string(open(path,'r').read())