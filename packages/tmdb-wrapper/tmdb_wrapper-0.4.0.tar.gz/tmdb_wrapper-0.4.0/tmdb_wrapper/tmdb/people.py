import textwrap
from typing import Any
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.data.person import Person, PersonChanges, PersonCredits, PersonExternalIds, PersonPopulars, PersonProfile, PersonTaggedImages, PersonTranslations
from tmdb_wrapper.tmdb.base import TMDb
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.request import  GetRequest

class People(TMDb):
    '''
    People Class
    '''
    def get_people_details(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None,
        append_to_response: str = None
        ) -> Any:

        '''
        Get the primary person details by id.

        Supports append_to_response. Read more about this .

        See more: https://developers.themoviedb.org/3/people/get-person-details
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}",
            append_to_response = append_to_response)

        return datatype.to_datatype(parse_data = parse_data, model_data = Person)

    def get_people_changes(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None,
        end_date: str = None,
        start_date: str = None,
        page: int = 1
        ) -> Any:

        '''
        Get the primary person details by id.

        Supports append_to_response. Read more about this .

        See more: https://developers.themoviedb.org/3/people/get-person-details
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/changes",
            start_date = start_date,
            end_date = end_date,
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonChanges)

    def get_people_movie_credits(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get the movie credits for a person.

        See more: https://developers.themoviedb.org/3/people/get-person-movie-credits
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/movie_credits")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonCredits)

    def get_people_tv_credits(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get the movie credits for a person.

        See more: https://developers.themoviedb.org/3/people/get-person-movie-credits
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/tv_credits")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonCredits)

    def get_people_combined_credits(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get the movie and TV credits together in a single response.

        See more: https://developers.themoviedb.org/3/people/get-person-combined-credits
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/combined_credits")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonCredits)

    def get_people_external_ids(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get the external ids for a person. We currently support the following external sources.

        External Sources
        IMDB ID
        Facebook
        Freebase MID
        Freebase ID
        Instagram
        TVRage ID
        Twitter

        See more: https://developers.themoviedb.org/3/people/get-person-external-ids
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/external_ids")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonExternalIds)

    def get_people_images(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get the images for a person.

        See more: https://developers.themoviedb.org/3/people/images
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/images")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonProfile)

    def get_people_tagged_images(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None,
        page: int = 1
        ) -> Any:

        '''
        Get the images that this person has been tagged in.

        See more: https://developers.themoviedb.org/3/people/tagged_images
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/tagged_images",
            page = page)

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonTaggedImages)

    def get_people_translations(
        self,
        datatype : Datatype = ModelDatatype(),
        person_id: int = None
        ) -> Any:

        '''
        Get a list of translations that have been created for a person.

        See more: https://developers.themoviedb.org/3/people/get-person-translations
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/person/{person_id}/translations")

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonTranslations)

    def get_people_latest(
        self,
        datatype : Datatype = ModelDatatype()
        ) -> Any:

        '''
        Get the most newly created person. This is a live response and will continuously change.

        See more: https://developers.themoviedb.org/3/people/get-latest-person
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/person/latest")

        return datatype.to_datatype(parse_data = parse_data, model_data = Person)

    def get_people_popular(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1
        ) -> Any:

        '''
        Get the most newly created person. This is a live response and will continuously change.

        See more: https://developers.themoviedb.org/3/people/get-latest-person
        '''


        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/person/popular",
            page = page)

        print(parse_data)

        return datatype.to_datatype(parse_data = parse_data, model_data = PersonPopulars)
