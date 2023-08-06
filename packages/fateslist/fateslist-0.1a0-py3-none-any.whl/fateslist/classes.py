import IBLPy.config as cfg
from IBLPy import api_modes, aiohttp
from typing import Union, Optional

class InvalidMode(Exception):
    """Raised when you don't have the required mode (package) to perform the action such as trying to do an asynchronous API request without having aiohttp_requests installed or trying to do a webhook without fastapi+uvicorn"""
    def __init__(self, mode):
        if mode == "async":
            super().__init__("In order to use IBLPy asynchronous API requests, you must have aiohttp_requests installed")
        elif mode == "fastapi":
            super().__init__("In order to use IBLPy webhooks, you must have fastapi and uvicorn installed")

class Ratelimit(Exception):
    """Raised when you are being ratelimited by IBL. The ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API"""
    def __init__(self):
        super().__init__("You are being ratelimited by the Infinity Bots (IBL) API. For future reference, the ratelimit for posting stats is 3 requests per 5 minutes and is unknown/variable for getting stats from the API!")

class APIResponse():
    """
        IBLAPIResponse represents an API response in the IBLPy library
        
        :param res: This is the raw response from the API. 
            This will be a aiohttp ClientResponse

        :param success: Whether the API response has succeeded or not (status less than 400)
        
        :param error_msg: The error message reported by the Infinity Bot List API

        :param message: Any messages returned by the API in the message field. Can be None if there are no messages

        :param json: The JSON object sent by the API

        :param status: The status code of the HTTP response received from the API
    """
    def __init__(self, *, res: aiohttp.ClientResponse, json: dict):
        self.res = res
        self.success = True if res.status < 400 else False
        self.message = json.get("message")
        self.error = json.get("error")
        self.json = json
        self.status = res.status

class BaseUser():
    """
        This is a base user on IBL from which all bots and users extend from
    """
    def __init__(self, id, json):
        self.__dict__.update(**json)
        self.id = id
        self.clean()
    
    def dict(self) -> dict:
        """Returns the class as a dict using the dict dunder property of the class"""
        return self.__dict__

    def __str__(self) -> str:
        """Returns the name of the bot or user"""
        return self.name

    def __int__(self) -> int:
        """Returns the bot or user ID"""
        return self.id
    
    def clean(self):
        """Cleans up all the ugly stuff from the IBL API"""
        for k, v in self.__dict__.items():
            self.__dict__[k] = self._cleaner(attr=v)
    
    def _cleaner(self, attr: str):
        if isinstance(attr, str):
            if attr == "none":
                return None
            elif attr == "false":
                return False
            elif attr == "true":
                return True
            elif attr.isdigit():
                return int(attr)
        
        elif isinstance(attr, dict):
            _tmp = {}
            for k, v in attr.items():
                _tmp[k] = self._cleaner(attr=v)
            return _tmp
        
        return attr
    
class Bot(BaseUser):
    """
        IBLBot is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). It represents a bot on IBL. The exact parameters of an IBLBot may change and IBLPy is designed to handle such changes automatically. Here are the parameters that we know of right now:
    """
    def __init__(self, id, json):
        super().__init__(id, json)
        
class User(BaseUser):
    """
        IBLUser is internally a part of the base_fn module (which provides all of IBLPy's base classes and functions). It represents a user on IBL. The exact parameters of an IBLUser may change and IBLPy is designed to handle such changes automatically. Here are the parameters that we know of right now:
    """
    def __init__(self, id, json):
        super().__init__(id, json)     
