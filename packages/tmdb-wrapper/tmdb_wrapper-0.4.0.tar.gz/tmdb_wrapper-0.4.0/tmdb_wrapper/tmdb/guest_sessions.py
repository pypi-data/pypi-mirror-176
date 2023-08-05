import textwrap
from typing import Any
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.request import GetRequest
from tmdb_wrapper.utils.constants import user_session


class GuestSessions(Authentication):
    '''
    Guest Session Class
    '''
    def __init__(self):
        super().__init__()
        if self.session_id is None or self.type_session == user_session:
            raise TMDbException(textwrap.fill(textwrap.dedent("""
            You need to initialize Authentication first and the type parameter must be guest_session""")))
    
    def get_guest_session_rated_movies(
        self,
        datatype : Datatype = ModelDatatype(),
        sort_by: str = None) -> Any:

        '''
        Get the rated movies for a guest session.

        See more: https://developers.themoviedb.org/3/guest-sessions/get-guest-session-rated-movies
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/guest_session/{self.session_id}/rated/movies",
            sort_by = sort_by)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_guest_session_rated_tv_shows(
        self,
        datatype : Datatype = ModelDatatype(),
        sort_by: str = None) -> Any:

        '''
        Get the rated TV shows for a guest session.

        See more: https://developers.themoviedb.org/3/genres/get-guest-session-rated-tv-shows
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/guest_session/{self.session_id}/rated/tv",
            sort_by = sort_by)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_guest_session_rated_tv_episodes(
        self,
        datatype : Datatype = ModelDatatype(),
        sort_by: str = None) -> Any:

        '''
        Get the rated TV episodes for a guest session.

        See more: https://developers.themoviedb.org/3/genres/get-gest-session-rated-tv-episodes
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/guest_session/{self.session_id}/rated/tv/episodes",
            sort_by = sort_by)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)