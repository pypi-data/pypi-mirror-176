import textwrap
from typing import Any
from tmdb_wrapper.data.review import Review
from tmdb_wrapper.data.search import Search, SearchMulti
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.request import  GetRequest

class Searches(TMDb):
    '''
    Search Class
    '''
    def get_search_company(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = "") -> Any:

        '''
        Search for companies.

        See more: https://developers.themoviedb.org/3/search/search-companies
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/company",
            page = page,
            query=query)

        return datatype.to_datatype(parse_data = parse_data, model_data = Search)

    def get_search_collections(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None) -> Any:

        '''
        Search for collections.

        See more: https://developers.themoviedb.org/3/search/search-collections
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/collection",
            page = page,
            query = query)

        return datatype.to_datatype(parse_data = parse_data, model_data = Search)

    def get_search_keywords(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None) -> Any:

        '''
        Search for keywords.

        See more: https://developers.themoviedb.org/3/search/search-keywords
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/keyword",
            page = page,
            query = query)

        return datatype.to_datatype(parse_data = parse_data, model_data = Search)

    def get_search_movie(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None,
        include_adult: bool = None,
        year: int = None,
        primary_realese_year: int = None) -> Any:

        '''
        Search for movies.

        See more: https://developers.themoviedb.org/3/search/search-keywords
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/movie",
            page = page,
            query = query,
            include_adult = include_adult,
            year = year,
            primary_realese_year = primary_realese_year)

        return datatype.to_datatype(parse_data = parse_data, model_data = Search)

    def get_multi_search(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None,
        include_adult: bool = None,
        year: int = None,
        primary_realese_year: int = None) -> Any:

        '''
        Search multiple models in a single request. Multi search currently supports searching for
        movies, tv shows and people in a single request.



        See more: https://developers.themoviedb.org/3/search/multi-search
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/movie",
            page = page,
            query = query,
            include_adult = include_adult,
            year = year,
            primary_realese_year = primary_realese_year)

        return datatype.to_datatype(parse_data = parse_data, model_data = SearchMulti)

    def get_search_people(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None,
        include_adult: bool = None,
        year: int = None,
        primary_realese_year: int = None) -> Any:

        '''
        Search for people.

        See more: https://developers.themoviedb.org/3/search/search-people
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/person",
            page = page,
            query = query,
            include_adult = include_adult,
            year = year,
            primary_realese_year = primary_realese_year)

        return datatype.to_datatype(parse_data = parse_data, model_data = SearchMulti)

    def get_search_tv_show(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1,
        query: str = None,
        include_adult: bool = None,
        year: int = None,
        primary_realese_year: int = None) -> Any:

        '''
        Search for a TV show.

        See more: https://developers.themoviedb.org/3/search/search-tv-shows
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/search/tv",
            page = page,
            query = query,
            include_adult = include_adult,
            year = year,
            primary_realese_year = primary_realese_year)
        
        return datatype.to_datatype(parse_data = parse_data, model_data = Search)