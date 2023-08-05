from abc import ABC, abstractmethod
import requests
from requests import Response


class Request(ABC):
    '''
    Abstract Class to get different requests
    '''
    @abstractmethod
    def request(self, url, params = None, data = None, headers = None, timeout = None) -> Response:
        pass


class GetRequest(Request):

    def request(self, url, params = None, data = None, headers = None, timeout = 5) -> Response:
        return requests.get(url = url, params = params, headers = headers, timeout= timeout)


class PostRequest(Request):

    def request(self, url, params = None, data = None, headers = None, timeout = 5) -> Response:
        return requests.post(url = url, params = params, data = data, headers = headers, timeout= timeout)


class DeleteRequest(Request):

    def request(self, url, params = None, data = None, headers = None, timeout = 5) -> Response:
        return requests.delete(url = url, params=params, data=data, headers = headers, timeout= timeout)


class PutRequest(Request):

    def request(self, url, params = None, data = None, headers = None, timeout = 5) -> Response:
        return requests.put(url = url, params = params, headers = headers, timeout= timeout)