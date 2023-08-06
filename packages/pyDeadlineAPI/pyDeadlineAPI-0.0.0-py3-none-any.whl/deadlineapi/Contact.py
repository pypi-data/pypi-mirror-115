
from deadlineapi.Validation import _is_email, _is_twitter

class Contact():
    def __init__(self,jsonobj,ignoreValidationErrors=False) -> None:

        if 'email' in jsonobj:
            try:
                _is_email(jsonobj['email'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e
            
            self.email = jsonobj['email']
        else:
            self.email = None


        if 'twitter' in jsonobj:
            try:
                _is_twitter(jsonobj['twitter'])
            except Exception as e:
                if ignoreValidationErrors:
                    pass
                else:
                    raise e
            
            self.twitter = jsonobj['twitter']
        else:
            self.twitter = None

    def to_str(self) -> str:
        if self.email is not None and self.twitter is not None:
            return f"{self.email}, {self.twitter}"
        elif self.email is not None:
            return f"{self.email}"
        elif self.twitter is not None:
            return f"{self.twitter}"
        else:
            return "No contact data available"