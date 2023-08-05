import os

from typing import Any
from tmdb_wrapper.data.authentication import GuestAuthentication, RequestTokenAuthentication, SessionAuthentication
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.datatype import Datatype, OriginalDatatype
from tmdb_wrapper.tmdb.request import DeleteRequest, GetRequest, PostRequest
from tmdb_wrapper.utils.helpers import read_pickle, save_pickle
from tmdb_wrapper.utils.constants import guest_session, user_session

class Authentication(TMDb):

    '''
    Authentication Class
    '''

    TMDB_USERNAME = "TMDB_USERNAME"
    TMDB_PASSWORD = "TMBD_PASSWORD"
    TMDB_SESSION_ID = "TMDB_SESSION_ID"
    TMDB_TYPE_SESSION= "TMDB_TYPE_SESSION"

    def __init__(
        self,
        username: str = None,
        password: str = None,
        route: str = "session_id.pkl"):

        super().__init__()
        self.username = username if username is not None else os.environ.get(self.TMDB_USERNAME, "username")
        self.password = password if password is not None else os.environ.get(self.TMDB_PASSWORD, "password")
        self.expires_at = None
        self.request_token = None
        self.route = route


    def initialize_session_id(
        self,
        type_session : str = guest_session) -> None:
        '''
        There are 2 types of sessions:
            guest_session
            user_session
        '''
        if type_session == guest_session:
            self.request_guest_session()
        elif type_session == user_session:
            try:
                session_information, same_id = read_pickle(route = self.route)
                self.user_session(
                    session_information=session_information,
                    same_id=same_id)
            except OSError:
                self.create_new_user_session(
                    route = self.route
                )
        else:
            raise TMDbException("You can only select 'guest_session' or 'user_session'")


    @property
    def username(self) -> str:
        return os.environ.get(self.TMDB_USERNAME)

    @username.setter
    def username(self, username: str) -> str:
        os.environ[self.TMDB_USERNAME] = username

    @property
    def password(self) -> str:
        return os.environ.get(self.TMDB_PASSWORD)

    @password.setter
    def password(self, password: str) -> str:
        os.environ[self.TMDB_PASSWORD] = password

    @property
    def session_id(self) -> str:
        return os.environ.get(self.TMDB_SESSION_ID)

    @session_id.setter
    def session_id(self, session_id: str) -> str:
        os.environ[self.TMDB_SESSION_ID] = session_id

    @property
    def type_session(self) -> str:
        return os.environ.get(self.TMDB_TYPE_SESSION)

    @type_session.setter
    def type_session(self, type_session: str) -> str:
        os.environ[self.TMDB_TYPE_SESSION] = type_session

    def request_guest_session(self):
        '''
        This function retrieve the guest session values.
        '''
        guest_session_resp = self.get_guest_session()
        self.expires_at, self.session_id = guest_session_resp['expires_at'], guest_session_resp['guest_session_id']
        os.environ[self.TMDB_SESSION_ID], os.environ[self.TMDB_TYPE_SESSION] = self.session_id, guest_session
       

    def get_guest_session(
        self,
        datatype : Datatype = OriginalDatatype()) -> Any:
        '''
        This method will let you create a new guest session. Guest sessions are a
        type of session that will let a user rate movies and TV shows but not require
        them to have a TMDB user account. More information about user authentication
        can be found .

        Please note, you should only generate a single guest session per user (or device)
        as you will be able to attach the ratings to a TMDB user account in the future.
        There is also IP limits in place so you should always make sure it's the end user
        doing the guest session actions.

        If a guest session is not used for the first time within 24 hours,
        it will be automatically deleted.

        See more: https://developers.themoviedb.org/3/authentication/create-guest-session
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/authentication/guest_session/new")

        return datatype.to_datatype(parse_data = parse_data, model_data = GuestAuthentication)


    def user_session(
        self,
        session_information : dict,
        same_id: bool):
        '''
        Function that checks if already exists a session id.
        If it does not exist it creates a new one.

        session_information: dict
            Dictionary with information of session_id, expires_at and request_token.

        same_id : bool
            Value that compares date of now with "expires_at" date. If
            expires_at > now it return False else return True.
        '''

        if same_id:
            self.expires_at = session_information['expires_at']
            self.session_id = session_information['session_id']
            self.request_token = session_information['request_token']
            os.environ[self.TMDB_SESSION_ID], os.environ[self.TMDB_TYPE_SESSION] = self.session_id, user_session

        else:
            self.create_new_user_session(
                route = self.route
            )
            os.environ[self.TMDB_SESSION_ID], os.environ[self.TMDB_TYPE_SESSION] = self.session_id, user_session

    def create_new_user_session(
        self,
        route: str):
        '''
        Creates a new user session id.
        '''

        self.request_token = self.get_request_token()['request_token']
        user_session_resp = self.post_create_session_with_login()
        self.expires_at = user_session_resp['expires_at']
        self.request_token = user_session_resp['request_token']
        self.session_id = self.post_create_session()['session_id']
        new_session_create = {
            'session_id': self.session_id,
            'expires_at': self.expires_at,
            'request_token': self.request_token
        }
        save_pickle(
            data = new_session_create,
            route = self.route)

    def get_request_token(
        self,
        datatype : Datatype = OriginalDatatype()) -> Any:
        '''
        Create a temporary request token that can be used to validate a TMDB user login.
        More details about how this works can be found .

        See more: https://developers.themoviedb.org/3/authentication/create-request-token
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/authentication/token/new")

        return datatype.to_datatype(parse_data = parse_data, model_data = RequestTokenAuthentication)

    def post_create_session(
        self,
        datatype : Datatype = OriginalDatatype()) -> Any:
        '''
        You can use this method to create a fully valid session ID once a user has
        validated the request token. More information about how this works can be found .

        See more: https://developers.themoviedb.org/3/authentication/create-session
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = "/authentication/session/new",
            data = {
                "request_token": self.request_token
            })

        return datatype.to_datatype(parse_data = parse_data, model_data = SessionAuthentication)

    def post_create_session_with_login(
        self,
        datatype : Datatype = OriginalDatatype()) -> Any:
        '''
        This method allows an application to validate a request token by entering
        a username and password.

        Not all applications have access to a web view so this can be used as a substitute.

        Please note, the preferred method of validating a request token is to have
        a user authenticate the request via the TMDB website. You can read about that method .

        If you decide to use this method please use HTTPS.

        See more: https://developers.themoviedb.org/3/authentication/validate-request-token
        '''
        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = "/authentication/token/validate_with_login",
            data={
            "username": self.username,
            "password": self.password,
            "request_token": self.request_token
            })

        return datatype.to_datatype(parse_data = parse_data, model_data = RequestTokenAuthentication)

    def post_create_session_from_v4(self):
        '''
        Use this method to create a v3 session ID if you already have a valid v4 access token.
        The v4 token needs to be authenticated by the user. Your standard "read token"
        will not validate to create a session ID.
        '''
        pass

    def delete_session(
        self,
        datatype : Datatype = OriginalDatatype()):
        '''
        If you would like to delete (or "logout") from a session, call this method with 
        a valid session ID.
        '''
        try:
            parse_data = self.request_data(
                request_operation = DeleteRequest(),
                path = "/authentication/session",
                data = {
                    "session_id": self.session_id
                    })

            os.remove(self.route)
            return datatype.to_datatype(parse_data = parse_data, model_data = RequestTokenAuthentication)
        except FileNotFoundError:
            print("Create a new session!!!")