import textwrap
from typing import Any
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.request import  GetRequest

class Trendings(TMDb):
    '''
    Trendings Class
    '''
    def get_trendings(
        self,
        datatype : Datatype = ModelDatatype(),
        media_type: str = "movie",
        time_window: str = "day") -> Any:

        '''
        Get the daily or weekly trending items. The daily trending list tracks items over the period of
        a day while items have a 24 hour half life. The weekly list tracks items over a 7 day period,
        with a 7 day half life.

        Valid Media Types

        Media_Type	   Description

        all	-> Include all movies, TV shows and people in the results as a global trending list.
        movie -> Show the trending movies in the results.
        tv -> Show the trending TV shows in the results.
        person -> Show the trending people in the results.

        Valid Time Windows

        Time_Window	Description

        day	-> View the trending list for the day.
        week -> View the trending list for the week.


        See more: https://developers.themoviedb.org/3/trending/get-trending
        '''

        media_type_lst = ["all", "movie", "tv", "person"]
        time_window_lst = ["day", "week"]

        if media_type not in media_type_lst or time_window not in time_window_lst:
            raise TMDbException("""You need to choose one of the values from ["all", "movie", "tv", "person"] for media_type.\n
            You need to choose one of the values from ["day", "week"] for time_window.""")


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/trending/{media_type}/{time_window}")

        return datatype.to_datatype(parse_data = parse_data, model_data = ModelMovies)
