from typing import Any
from tmdb_wrapper.data.configuration import Configuration, ConfigurationCountry, ConfigurationJobs, ConfigurationLanguage, ConfigurationPrimTranslations, ConfigurationTimezones
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.request import GetRequest
from .base import TMDb

class Configurations(TMDb):
    '''
    requests that are represented by Companies
    '''
    def get_configuration(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the system wide configuration information. Some elements of the API require some
        knowledge of this configuration data. The purpose of this is to try and keep the actual
        API responses as light as possible. It is recommended you cache this data within your
        application and check for updates every few days.

        This method currently holds the data relevant to building image URLs as well as the change key map.

        To build an image URL, you will need 3 pieces of data. The base_url, size and file_path. 
        Simply combine them all and you will have a fully qualified URL. Here’s an example URL:

        https://image.tmdb.org/t/p/w500/8uO0gUM8aNqYLs1OsTBQiXu0fEv.jpg
        The configuration method also contains the list of change keys which can be useful 
        if you are building an app that consumes data from the change feed.

        See more: https://developers.themoviedb.org/3/configuration/get-api-configuration
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration")

        return datatype.to_datatype(parse_data = parse_data, model_data = Configuration)

    def get_configuration_country(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list of countries (ISO 3166-1 tags) used throughout TMDB.

        See more: https://developers.themoviedb.org/3/companies/get-countries
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration/countries")

        return datatype.to_datatype(parse_data = parse_data, model_data = ConfigurationCountry)

    def get_configuration_job(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get a list of the jobs and departments we use on TMDB.

        See more: https://developers.themoviedb.org/3/companies/get-jobs
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration/jobs")

        return datatype.to_datatype(parse_data = parse_data, model_data = ConfigurationJobs)

    def get_configuration_language(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list of languages (ISO 639-1 tags) used throughout TMDB.

        See more: https://developers.themoviedb.org/3/companies/get-languages
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration/languages")

        return datatype.to_datatype(parse_data = parse_data, model_data = ConfigurationLanguage)
    
    def get_configuration_primary_translations(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get a list of the officially supported translations on TMDB.

        While it's technically possible to add a translation in any one
        of the  we have added to TMDB (we don't restrict content), the ones
        listed in this method are the ones we also support for localizing the
        website with which means they are what we refer to as the "primary" translations.

        These are all specified as  to identify the languages we use on TMDB.
        There is one exception which is image languages. They are currently 
        only designated by a ISO-639-1 tag. This is a planned upgrade for the future.

        We're always open to adding more if you think one should be added.
        You can ask about getting a new primary translation added by posting on .

        One more thing to mention, these are the translations that map to
        our website translation project. You can view and contribute to that project .

        See more: https://developers.themoviedb.org/3/companies/get-primary-translations
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration/primary_translations")

        return datatype.to_datatype(
        parse_data = parse_data,
        model_data = ConfigurationPrimTranslations)

    def get_configuration_timezones(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:

        '''
        Get the list of timezones used throughout TMDB.

        See more: https://developers.themoviedb.org/3/companies/get-timezones
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/configuration/timezones")

        return datatype.to_datatype(
        parse_data = parse_data,
        model_data = ConfigurationTimezones)
    

    