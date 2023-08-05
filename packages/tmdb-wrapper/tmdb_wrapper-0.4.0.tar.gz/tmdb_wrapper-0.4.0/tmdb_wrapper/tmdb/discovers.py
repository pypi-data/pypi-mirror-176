from tkinter import N
from typing import Any
from tmdb_wrapper.data.discover import Discover
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Discovers(TMDb):
    '''
    requests that are represented by Discovers
    '''
    def get_movie_discover(
        self,
        datatype : Datatype = ModelDatatype(),
        sort_by: str = None,
        certification_country: str = None,
        certification: str = None,
        certification_lte: str = None,
        certification_gte: str = None,
        include_adult: bool = None,
        include_video: bool = None,
        page: int = 1,
        primary_realese_year: int = None,
        primary_relase_date_gte: str = None,
        primary_relase_date_lte: str = None,
        release_date_gte: str = None,
        release_date_lte: str = None,
        with_release_type: int = None,
        year: int = None,
        vote_count_gte: int = None,
        vote_count_lte: int = None,
        vote_average_gte: int = None,
        vote_average_lte: int = None,
        with_cast: str = None,
        with_crew: str = None,
        with_people: str = None,
        with_companies: str = None,
        with_genres: str = None,
        without_genres: str = None,
        with_keywords: str = None,
        without_keywords: str = None,
        with_runtime_gte: int = None,
        with_runtime_lte: int = None,
        with_original_language: str = None,
        with_watch_providers: str = None,
        watch_region: str = None,
        with_watch_monetizion_types: str = None,
        without_companies: str = None
        ) -> Any:

        '''
        Discover movies by different types of data like average rating, number of votes,
        genres and certifications. You can get a valid list of certifications from the  method.

        Discover also supports a nice list of sort options. See below for all of the
        available options.

        Please note, when using certification \ certification.lte you must also specify
        certification_country. These two parameters work together in order to filter the
        results. You can only filter results with the countries we have added to our .

        If you specify the region parameter, the regional release date will be used instead
        of the primary release date. The date returned will be the first date based on your
        query (ie. if a with_release_type is specified). It's important to note the order of
        the release types that are used. Specifying "2|3" would return the limited theatrical
        release date as opposed to "3|2" which would return the theatrical date.

        Also note that a number of filters support being comma (,) or pipe (|) separated.
        Comma's are treated like an AND and query while pipe's are an OR.

        Some examples of what can be done with discover can be found .

        See more: https://developers.themoviedb.org/3/discover/movie-discover
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/discover/movie",
            sort_by = sort_by,
            certification_country = certification_country,
            certification = certification,
            certification_lte = certification_lte,
            certification_gte = certification_gte,
            include_adult = include_adult,
            include_video = include_video,
            page = page,
            primary_realese_year = primary_realese_year,
            primary_relase_date_gte = primary_relase_date_gte,
            primary_relase_date_lte = primary_relase_date_lte,
            release_date_gte = release_date_gte,
            release_date_lte = release_date_lte,
            with_release_type = with_release_type,
            year = year,
            vote_count_gte = vote_count_gte,
            vote_count_lte = vote_count_lte,
            vote_average_gte = vote_average_gte,
            vote_average_lte = vote_average_lte,
            with_cast = with_cast,
            with_crew = with_crew,
            with_people = with_people,
            with_companies = with_companies,
            with_genres = with_genres,
            without_genres = without_genres,
            with_keywords = with_keywords,
            without_keywords = without_keywords,
            with_runtime_gte = with_runtime_gte,
            with_runtime_lte = with_runtime_lte,
            with_original_language = with_original_language,
            with_watch_providers = with_watch_providers,
            watch_region = watch_region,
            with_watch_monetizion_types = with_watch_monetizion_types,
            without_companies = without_companies)

        return datatype.to_datatype(parse_data = parse_data, model_data = Discover)

    def get_tv_discover(
        self,
        datatype : Datatype = ModelDatatype(),
        sort_by: str = None,
        air_date_gte: str = None,
        air_date_lte: str = None,
        first_air_date_gte: str = None,
        first_air_date_lte: str = None,
        first_air_date_year: str = False,
        page: int = 1,
        timezone: str = None,
        vote_count_gte: int = None,
        vote_average_gte: int = None,
        with_genres: str = None,
        with_networks: str = None,
        without_genres: str = None,
        with_runtime_gte: int = None,
        with_keywords: str = None,        
        with_runtime_lte: int = None,
        without_keywords: str = None,
        include_null_first_air_dates: bool = None,
        with_original_language: str = None,
        screened_theatrically: bool = None,
        with_companies: str = None,
        with_watch_providers: str = None,
        watch_region: str = None,
        with_watch_monetization_types: str = None,
        with_status: str = None,
        with_type: str = None,
        without_companies: str = None
        ) -> Any:

        '''
        Discover TV shows by different types of data like average rating, number of
        votes, genres, the network they aired on and air dates.

        Discover also supports a nice list of sort options. See below for all of the
        available options.

        Also note that a number of filters support being comma (,) or pipe (|) separated.
        Comma's are treated like an AND and query while pipe's are an OR.

        Some examples of what can be done with discover can be found .

        See more: https://developers.themoviedb.org/3/discover/tv-discover
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/discover/tv",
            sort_by = sort_by,
            air_date_gte = air_date_gte,
            air_date_lte = air_date_lte,
            first_air_date_gte = first_air_date_gte,
            first_air_date_lte = first_air_date_lte,
            first_air_date_year = first_air_date_year,
            page = page,
            timezone = timezone,
            vote_count_gte = vote_count_gte,
            vote_average_gte = vote_average_gte,
            with_genres = with_genres,
            with_networks = with_networks,
            without_genres = without_genres,
            with_runtime_gte = with_runtime_gte,
            with_keywords = with_keywords,        
            with_runtime_lte = with_runtime_lte,
            without_keywords = without_keywords,
            include_null_first_air_dates = include_null_first_air_dates,
            with_original_language = with_original_language,
            screened_theatrically = screened_theatrically,
            with_companies = with_companies,
            with_watch_providers = with_watch_providers,
            watch_region = watch_region,
            with_watch_monetization_types = with_watch_monetization_types,
            with_status = with_status,
            with_type = with_type,
            without_companies = without_companies)

        return datatype.to_datatype(parse_data = parse_data, model_data = Discover)
