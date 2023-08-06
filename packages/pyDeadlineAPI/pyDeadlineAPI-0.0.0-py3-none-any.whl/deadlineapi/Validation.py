

from urllib.parse import urlparse
import json

import jsonschema

def _is_url(s) -> bool:
        try:
            result = urlparse(s)
            return all([result.scheme, result.netloc])
        except:
            raise Exception(f"{s} is no valid url.")

def _is_twitter(s) -> bool:
    if not s[0] == '@' and len(s) > 1:
        raise Exception(f"{s} is no valid twitter account")

def _is_email(s) -> bool:
    pass

def _is_api_version(s) -> bool:
    splitted = s.split('.')
    if len(splitted) <= 1:
        raise Exception(f"A valid api version must have at least 2 two parts but {s} has less.")
    try:
        int(splitted[0])
        int(splitted[1])
    except:
        raise Exception(f"A valid api version must consist of two numbers but {s} does not.")

def _is_valid_date(s) -> bool:
    # TODO
    return True

def _is_valid_deadline(s) -> bool:
    # TODO
    return True


schema = json.loads("""{
    "$id": "https://schema.deadlineapi.org/schema_0.1.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "DeadlineAPI v0.1",
    "type": "object",
    "properties": {
        "api_compatibility": {
            "description": "The versions your DeadlineAPI endpoint supports. This should at least contain 0.1.",
            "type": "array",
            "items": {
                "type": "string"
            },
            "contains": {
                "const": "0.1"
            }
        },
        "name": {
            "description": "The name of your endpoint",
            "type": "string"
        },
        "url": {
            "description": "The URL of your endpoint",
            "type": "string"
        },
        "logo": {
            "description": "URL to your endpoint logo",
            "type": "string"
        },
        "deadlines": {
            "description": "Here come the list with the actual conference deadlines",
            "type": "array",
            "items": {
                "required": [
                    "name",
                    "deadline",
                    "startdate",
                    "location",
                    "contact"

                ],
                "type": "object",
                "properties": {
                    "name": {
                        "description": "The name of the conference",
                        "type": "string"
                    },
                    "shortname": {
                        "description": "The abbreviation of the conference.",
                        "type": "string"
                    },
                    "logo": {
                        "description": "URL to your conference logo",
                        "type": "string"
                    },
                    "cfpurl": {
                        "description": "URL to the conference's call for paper",
                        "type": "string"
                    },
                    "confurl": {
                        "description": "URL to the conference website",
                        "type": "string"
                    },
                    "location": {
                        "description": "Position data such as a postal address or geographic coordinates",
                        "type": "object",
                        "properties": {
                            "virtual": {
                                "description": "Set to true if the conference is virtual. False otherwise. If the conference is not virtual than please fill the fields country and city.",
                                "type": "boolean"
                            },
                            "country": {
                                "description": "The country in which the conference takes place",
                                "type": "string"
                            },
                            "city": {
                                "description": "The city in which the conference takes place",
                                "type": "string"
                            },
                            "lat": {
                                "description": "Latitude of the conference venue, in degree with decimal places. Use positive values for locations north of the equator, negative values for locations south of equator.",
                                "type": "number"
                            },
                            "lon": {
                                "description": "Longitude of the conference venue, in degree with decimal places. Use positive values for locations east of Greenwich, and negative values for locations west of Greenwich.",
                                "type": "number"
                            }
                        },
                        "required": [
                            "virtual"
                        ]
                    },
                    "contact": {
                        "description": "Contact information for the conference.",
                        "type": "object",
                        "properties": {
                            "twitter": {
                                "description": "Twitter handle, with leading @",
                                "type": "string"
                            },
                            "email": {
                                "description": "E-mail address for contacting the conference.",
                                "type": "string"
                            }
                        }
                    },
                    "startdate": {
                        "description": "The start date of the conference. In the following format yyyy-MM-dd. Example: 2021-08-06",
                        "type": "string"
                    },
                    "enddate": {
                        "description": "The end date of the conference. In the following format yyyy-MM-dd. Example: 2021-08-06",
                        "type": "string"
                    },
                    "deadline": {
                        "description": "The actual deadline of the conference or the workshop. In the following format yyyy-MM-dd HH:mm:ss ZZZZ. Example 2017-08-19 12:17:55 -0400. Make sure to use the correct timezone",
                        "type": "string"
                    },
                    "pagelimit": {
                        "description": "The pagelimit, if available.",
                        "type": "integer"
                    },
                    "categories": {
                        "description": "Research fields covered by the conference.",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}
""")


def _is_valid_schema_by_jsonobj(jsonobj) -> bool:
    jsonschema.validate(jsonobj,schema)
