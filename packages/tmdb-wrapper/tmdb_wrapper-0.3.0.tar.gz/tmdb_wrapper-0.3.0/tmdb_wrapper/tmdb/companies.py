from typing import Any
from tmdb_wrapper.data.company import Company, CompanyAlternativeNames, CompanyImage
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Companies(TMDb):
    '''
    requests that are represented by Companies
    '''
    def get_company_details(
        self,
        company_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get collection details by id.

        See more: https://developers.themoviedb.org/3/companies/get-company-details
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/company/{company_id}")

        return datatype.to_datatype(parse_data = parse_data, model_data = Company)

    def get_company_alternative_names(
        self,
        company_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the alternative names of a company.

        See more: https://developers.themoviedb.org/3/companies/get-company-alternative-names
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/company/{company_id}/alternative_names")

        return datatype.to_datatype(parse_data = parse_data, model_data = CompanyAlternativeNames)

    def get_company_images(
        self,
        company_id,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get a companies logos by id.

        There are two image formats that are supported for companies, PNG's and SVG's. You can see 
        which type the original file is by looking at the file_type field. We prefer SVG's as 
        they are resolution independent and as such, the width and height are only there to 
        reflect the original asset that was uploaded. An SVG can be scaled properly beyond 
        those dimensions if you call them as a PNG.

        See more: https://developers.themoviedb.org/3/companies/get-company-images
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = f"/company/{company_id}/images")

        return datatype.to_datatype(parse_data = parse_data, model_data = CompanyImage)