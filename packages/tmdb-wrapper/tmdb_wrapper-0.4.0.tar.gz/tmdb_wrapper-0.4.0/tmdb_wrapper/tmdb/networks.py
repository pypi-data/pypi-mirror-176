from typing import Any
from tmdb_wrapper.data.network import Network, NetworkAlternativeNames, NetworkImage
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Networks(TMDb):
    '''
    Get the details of a network.
    '''
    def get_network_details(
        self,
        network_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the details of a network.

        See more: https://developers.themoviedb.org/3/networks/get-network-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/network/{network_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Network)

    def get_network_alternative_names(
        self,
        network_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the details of a network.

        See more: https://developers.themoviedb.org/3/networks/get-network-alternative-names
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/network/{network_id}/alternative_names")

        print(parse_data)

        return datatype.to_datatype(parse_data = parse_data, model_data = NetworkAlternativeNames)

    def get_network_images(
        self,
        network_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the TV network logos by id.

        There are two image formats that are supported for networks, PNG's and SVG's.
        You can see which type the original file is by looking at the file_type field.
        We prefer SVG's as they are resolution independent and as such, the width and
        height are only there to reflect the original asset that was uploaded. An SVG
        can be scaled properly beyond those dimensions if you call them as a PNG.

        For more information about how SVG's and PNG's can be used, take a read through .

        See more: https://developers.themoviedb.org/3/networks/get-network-images
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/network/{network_id}/images")

        return datatype.to_datatype(parse_data = parse_data, model_data = NetworkImage)