import textwrap
from typing import Any
from tmdb_wrapper.data.detail import Detail
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.data.status import Status
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype, OriginalDatatype
from tmdb_wrapper.tmdb.request import GetRequest, PostRequest
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.utils.constants import user_session

class Account(Authentication):
    
    def __init__(self):
        super().__init__()
        if self.session_id is not None and self.type_session == user_session:
            self.details = self.get_details(datatype = ModelDatatype())
            self.account_id = self.details.id
        else:
            raise TMDbException(textwrap.fill(textwrap.dedent("""
            You need to initialize Authentication first. Try use:\n authentication = Authentication(username="username",password="password")\n
            authentication.initialize_session_id(type_session='user_session')""")))
        

    def get_details(
        self,
        datatype : Datatype = OriginalDatatype()) -> Any:
        '''
        Get your account details.

        See more: https://developers.themoviedb.org/3/account/get-account-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/account",
            session_id=self.session_id)
        
        return datatype.to_datatype(parse_data = parse_data, model_data = Detail)

    def get_created_lists(
        self,
        datatype : Datatype = OriginalDatatype(),
        page: int = 1) -> Any:
        '''
        Get all of the lists created by an account. Will invlude private lists if you are the owner.


        See more: https://developers.themoviedb.org/3/account/get-created-lists
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/lists",
            session_id = self.session_id,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_favourite_movies(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get the list of your favorite movies.


        See more: https://developers.themoviedb.org/3/account/get-favorite-movies
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/favorite/movies",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_favourite_tvs(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get the list of your favorite TV shows.


        See more: https://developers.themoviedb.org/3/account/get-favorite-tv-shows
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/favorite/tv",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def post_mark_as_favourite(
        self,
        datatype : Datatype = OriginalDatatype(),
        media_type: str = None,
        media_id: str = None,
        favorite: str = None
        ) -> Any:
        '''
        This method allows you to mark a movie or TV show as a favorite item.

        See more: https://developers.themoviedb.org/3/account/mark-as-favorite
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = f"/account/{self.account_id}/favorite",
            data={"media_type":media_type,"media_id":media_id,"favorite":favorite},
            headers= {'content-type': 'application/x-www-form-urlencoded'},
            session_id = self.session_id)

        

        return datatype.to_datatype(parse_data = parse_data, model_data = Status)

    def get_rated_movies(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get a list of all the movies you have rated.


        See more: https://developers.themoviedb.org/3/account/get-rated-movies
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/rated/movies",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_tv_shows(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get a list of all the TV shows you have rated.

        See more: https://developers.themoviedb.org/3/account/get-rated-tv-shows
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/rated/tv",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_tv_episodes(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get a list of all the TV episodes you have rated.

        See more: https://developers.themoviedb.org/3/account/get-rated-tv-episodes
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/rated/tv/episodes",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_movies_watchlist(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get a list of all the movies you have added to your watchlist.

        See more: https://developers.themoviedb.org/3/account/get-movie-watchlist
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/watchlist/movies",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def get_tv_show_watchlist(
        self,
        datatype : Datatype = OriginalDatatype(),
        sort_by: str = None,
        page: int = 1
        ) -> Any:
        '''
        Get a list of all the TV shows you have added to your watchlist.

        See more: https://developers.themoviedb.org/3/account/get-tv-show-watchlist
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/account/{self.account_id}/watchlist/tv",
            session_id = self.session_id,
            sort_by = sort_by,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)

    def post_add_to_watchlist(
        self,
        datatype : Datatype = OriginalDatatype(),
        media_type: str = None,
        media_id: str = None,
        watchlist: str = None
        ) -> Any:
        '''
        Add a movie or TV show to your watchlist.

        See more: https://developers.themoviedb.org/3/account/add-to-watchlist
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = f"/account/{self.account_id}/watchlist",
            data={
                "media_type":media_type,
                "media_id":media_id,
                "watchlist":watchlist},
            headers= {'content-type': 'application/x-www-form-urlencoded'},
            session_id = self.session_id)

        return datatype.to_datatype(parse_data = parse_data, model_data = Status)
