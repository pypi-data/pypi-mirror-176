import textwrap
from typing import Any
from tmdb_wrapper.data.list import ListModel, ListResponse
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException
from tmdb_wrapper.tmdb.request import DeleteRequest, GetRequest, PostRequest
from tmdb_wrapper.tmdb.authentication import Authentication
from tmdb_wrapper.utils.constants import url_header_encoded,guest_session

class Lists(Authentication):
    '''
    List Class
    '''
    def __init__(self):
        super().__init__()
        if self.session_id is None or self.type_session == guest_session:
            raise TMDbException(textwrap.fill(textwrap.dedent("""
                You need to initialize Authentication first. Try use:\n authentication = Authentication(username="username",password="password")\n
                authentication.initialize_session_id(type_session='user_session')""")))


    def get_list_details(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: int = 1) -> Any:

        '''
        Get the details of a list.

        See more: https://developers.themoviedb.org/3/lists/get-list-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/list/{list_id}")

        print(parse_data)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListModel)

    def get_list_items_status(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: int = 1,
        movie_id: int = 1) -> Any:

        '''
        You can use this method to check if a movie has already been added to the list.

        See more: https://developers.themoviedb.org/3/lists/check-item-status
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/list/{list_id}",
            movie_id = movie_id)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListModel)

    def post_create_list(
        self,
        datatype : Datatype = ModelDatatype(),
        name: str = None,
        description: str = None,
        language: str = None) -> Any:

        '''
        Create a list.

        See more: https://developers.themoviedb.org/3/lists/create-list
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = "/list",
            data = {
                "name":name,
                "description":description,
                "language": language
            },
            session_id = self.session_id,
            headers= url_header_encoded)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListResponse)

    def post_add_movie_to_list(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: str = None,
        media_id: int = None) -> Any:

        '''
        Add a movie to a list.

        See more: https://developers.themoviedb.org/3/lists/add-movie
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = f"/list/{list_id}/add_item",
            data = {
                "media_id":media_id
            },
            session_id = self.session_id,
            headers= url_header_encoded)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListResponse)

    def post_remove_movie(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: str = None,
        media_id: int = None) -> Any:

        '''
        Remove a movie from a list.

        See more: https://developers.themoviedb.org/3/lists/remove-movie
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = f"/list/{list_id}/remove_item",
            data = {
                "media_id":media_id
            },
            session_id = self.session_id,
            headers= url_header_encoded)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListResponse)

    def post_clear_list(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: str = None) -> Any:

        '''
        Clear all of the items from a list.

        See more: https://developers.themoviedb.org/3/lists/clear-list
        '''

        parse_data = self.request_data(
            request_operation = PostRequest(),
            path = f"/list/{list_id}/clear",
            headers = url_header_encoded,
            session_id = self.session_id,
            confirm = "true")

        return datatype.to_datatype(parse_data = parse_data, model_data = ListResponse)

    def delete_list(
        self,
        datatype : Datatype = ModelDatatype(),
        list_id: str = None) -> Any:

        '''
        Delete a list.

        See more: https://developers.themoviedb.org/3/lists/delete-list
        '''

        parse_data = self.request_data(
            request_operation = DeleteRequest(),
            path = f"/list/{list_id}",
            session_id = self.session_id)

        return datatype.to_datatype(parse_data = parse_data, model_data = ListResponse)
    
