from typing import Any
from tmdb_wrapper.data.collection import Collection, CollectionImage, CollectionTranslation
from tmdb_wrapper.data.movie import ModelMovies
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Collections(TMDb):
    '''
    requests that are represented by Collections
    '''
    def get_details_collection(
        self,
        collection_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get collection details by id.

        See more: https://developers.themoviedb.org/3/collections/get-collection-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/collection/{collection_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Collection)

    def get_image_collection(
        self,
        collection_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get collection details by id.

        See more: https://developers.themoviedb.org/3/collections/get-collection-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/collection/{collection_id}/images")

        return datatype.to_datatype(parse_data = parse_data, model_data = CollectionImage)

    def get_translation_collection(
        self,
        collection_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list translations for a collection by id.

        See more: https://developers.themoviedb.org/3/collections/get-collection-translations
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/collection/{collection_id}/translations")

        return datatype.to_datatype(parse_data = parse_data, model_data = CollectionTranslation)
