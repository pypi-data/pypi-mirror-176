import os
from typing import final
from .parse import ParseData
from .request import Request
from tmdb_wrapper.utils.constants import TMDB_URL,TMDB_VERSION

# from constants import TMDB_URL, TMDB_VERSION


class TMDb(object):
    '''
    Main Class of the project
    '''

    TMDB_KEY = "TMDB_KEY"
    TMDB_LANGUAGE = "TMDB_LANGUAGE"
    TMDB_REGION = "TMDB_REGION"

    def __init__(
        self,
        api_key : str = None,
        language : str = None,
        region : str = None,):

        self.api_key = api_key if api_key is not None else os.environ.get(self.TMDB_KEY, "API_KEY")
        self.language = language if language is not None else os.environ.get(self.TMDB_LANGUAGE, "en-US")
        self.region = region if region is not None else os.environ.get(self.TMDB_REGION, "US")

    @property
    def host(self) -> str:
        '''
        get Host
        '''
        return TMDB_URL

    @property
    def version(self) -> str:
        '''
        get Version
        '''
        return TMDB_VERSION

    @property
    def api_key(self) -> str:
        return os.environ.get(self.TMDB_KEY)

    @api_key.setter
    def api_key(self, key: str) -> None:
        os.environ[self.TMDB_KEY] = key

    @property
    def language(self) -> str:
        return os.environ.get(self.TMDB_LANGUAGE)

    @language.setter
    def language(self, language: str) -> None:
        os.environ[self.TMDB_LANGUAGE] = language

    @property
    def region(self) -> str:
        return os.environ.get(self.TMDB_REGION)

    @region.setter
    def region(self, region: str) -> None:
        os.environ[self.TMDB_REGION] = region


    @property
    def default_parameters(self) -> dict:
        '''
        get url parameters
        '''

        return {
            "api_key": self.api_key,
            "language": self.language,
            "region": self.region
        }

    def request_data(
        self,
        request_operation: Request,
        path: str,
        data: dict = None,
        headers: dict = None,
        **kwargs) -> ParseData:
        '''
        Request Data to Movie API
        '''
        def helper_params(args : dict) -> dict:
            params = {}

            for key, value in args.items():
                if value is not None:
                    if value is True:
                        params[key.replace("__",".")] = "true"
                    elif value is False:
                        params[key.replace("__",".")] = "false"
                    else:
                        params[key.replace("__",".")] = value
            return params

        additional_params = helper_params(kwargs)

        url = f'{self.host}/{self.version}/{path}'

        final_params = {**self.default_parameters, **additional_params}

        response = request_operation.request(
            url = url,
            params = final_params,
            data = data,
            headers=headers).json()

        # transform list -> dict
        if isinstance(response, list):
            response = dict(enumerate(response))

        return ParseData(response)
