from typing import Any
from tmdb_wrapper.data.image import Images

from tmdb_wrapper.tmdb.authentication import Authentication

from tmdb_wrapper.data.external_id import ExternalIDs
from tmdb_wrapper.data.keyword import Keywords
from tmdb_wrapper.data.tv import Tv, TvAccountState, TvAiring, TvAlternativeTitles, TvChanges, TvCredits, TvEpisodeGroups, TvRatings, TvRecommendations, TvScreens, TvSimilars, TvTranslations, TvVideos
from tmdb_wrapper.tmdb.datatype import Datatype, ModelDatatype
from tmdb_wrapper.tmdb.excep import TMDbException

from tmdb_wrapper.utils.constants import url_header_encoded

from .request import DeleteRequest, GetRequest, PostRequest

class Tvs(Authentication):
    '''
    TODO: Get Watch Providers GET
    '''

    def __init__(self):
        super().__init__()
        if self.session_id is None:
            raise TMDbException("You need to initialize a guest session or user session'")


    def get_details(
        self,
        tv_id: int, 
        datatype : Datatype = ModelDatatype(),
        append_to_response: str = None) -> Any:
        '''
        Grab the following account states for a session:

        TV show rating
        If it belongs to your watchlist
        If it belongs to your favourite list

        See more: https://developers.themoviedb.org/3/tv/get-tv-account-states
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(), 
            path = f"/tv/{tv_id}",
            append_to_response = append_to_response)

        return datatype.to_datatype(parse_data = parse_data, model_data = Tv)

    def get_account_states(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        append_to_response: str = None) -> Any:
        '''
        Get all the details about a movie.

        See more: https://developers.themoviedb.org/3/movies/get-movie-details
        '''

        def init_session_type(**kwargs):
            return self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/account_states",
                append_to_response = append_to_response,
                **kwargs)

        if self.type_session == "guest_session":
            parse_data = init_session_type(guest_session_id = self.session_id)

        else:
            parse_data = init_session_type(session_id = self.session_id)

        return datatype.to_datatype(parse_data = parse_data, model_data = TvAccountState)

    def get_aggregate_credits(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
       Get the aggregate credits (cast and crew) that have been added to a TV show.

       This call differs from the main credits call in that it does not return the newest 
       season but rather, is a view of all the entire cast & crew for all episodes belonging to a TV show.

        See more: https://developers.themoviedb.org/3/movies/get-tv-aggregate-credits
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/aggregate_credits")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvCredits)

    def get_alternative_titles(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Returns all of the alternative titles for a TV show.

        See more: https://developers.themoviedb.org/3/movies/get-tv-alternative-titles
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/alternative_titles")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvAlternativeTitles)

    def get_changes(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        start_date: str = None,
        end_date: str = None,
        page: int = 1) -> Any:
        '''
        Get the changes for a TV show. By default only the last 24 hours are returned.

        You can query up to 14 days in a single query by using the start_date and end_date query
        parameters.

        TV show changes are different than movie changes in that there are some edits on seasons and
        episodes that will create a change entry at the show level. These can be found under the
        season and episode keys. These keys will contain a series_id and episode_id. You can
        use the  and  methods to look these up individually.

        See more: https://developers.themoviedb.org/3/movies/get-tv-changes
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/changes",
                start_date = start_date,
                end_date = end_date,
                page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvChanges)

    def get_content_ratings(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the list of content ratings (certifications) that have been added to a TV show.

        See more: https://developers.themoviedb.org/3/movies/get-tv-content-ratings
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/content_ratings")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvRatings)

    def get_credits(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the credits (cast and crew) that have been added to a TV show.

        See more: https://developers.themoviedb.org/3/tv/get-tv-credits
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/credits")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvCredits)

    def get_episode_group(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get all of the episode groups that have been created for a TV show. With a group ID you can call the  method.

        See more: https://developers.themoviedb.org/3/tv/get-tv-episode-groups
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/episode_groups")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvEpisodeGroups)

    def get_external_ids(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the external ids for a TV show. We currently support the following external sources.

        See more: https://developers.themoviedb.org/3/tv/get-tv-external-ids
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/external_ids")


        return datatype.to_datatype(parse_data = parse_data, model_data = ExternalIDs)

    def get_images(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the images that belong to a TV show.

        Querying images with a language parameter will filter the results.
        If you want to include a fallback language (especially useful for backdrops)
        you can use the include_image_language parameter. This should be a comma
        seperated value like so: include_image_language=en,null.

        See more: https://developers.themoviedb.org/3/tv/get-tv-images
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/images")


        return datatype.to_datatype(parse_data = parse_data, model_data = Images)

    def get_keywords(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the keywords that have been added to a TV show.


        See more: https://developers.themoviedb.org/3/tv/get-tv-keywords
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/keywords")


        return datatype.to_datatype(parse_data = parse_data, model_data = Keywords)

    def get_recommendations(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get the list of TV show recommendations for this item.


        See more: https://developers.themoviedb.org/3/tv/get-tv-recommendations
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/recommendations",
                page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvRecommendations)

    def get_reviews(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get the list of TV show recommendations for this item.


        See more: https://developers.themoviedb.org/3/tv/get-tv-recommendations
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/recommendations",
                page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvRecommendations)

    def get_screened_theatrically(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get a list of seasons or episodes that have been screened in a film festival or theatre.

        See more: https://developers.themoviedb.org/3/tv/get-screened-theatrically
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/recommendations")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvScreens)

    def get_similar(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of similar TV shows. These items are assembled by looking at keywords and genres.

        See more: https://developers.themoviedb.org/3/tv/get-similar-tv-shows
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/similar",
                page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvSimilars)

    def get_translations(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get a list of the translations that exist for a TV show.

        See more: https://developers.themoviedb.org/3/tv/get-tv-translations
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/translations")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvTranslations)

    def get_videos(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the videos that have been added to a TV show.

        See more: https://developers.themoviedb.org/3/tv/get-tv-videos
        '''

        parse_data = self.request_data(
                request_operation = GetRequest(),
                path = f"/tv/{tv_id}/videos")


        return datatype.to_datatype(parse_data = parse_data, model_data = TvVideos)

    def get_watch_providers(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the videos that have been added to a TV show.

        See more: https://developers.themoviedb.org/3/tv/get-tv-videos
        '''

    def post_rate_video(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype(),
        value: float = 0.5) -> Any:
        '''
        A valid session or guest session ID is required. You can read more about how this works .

        See more: https://developers.themoviedb.org/3/tv/rate-tv-show
        '''

        def init_session_type(**kwargs):
            return self.request_data(
                request_operation = PostRequest(),
                path = f"/tv/{tv_id}/rating",
                data = {
                "value":value
                },
                headers=url_header_encoded,
                **kwargs)

        if self.type_session == "guest_session":
            parse_data = init_session_type(guest_session_id = self.session_id)

        else:
            parse_data = init_session_type(session_id = self.session_id)


        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = TvVideos)

    def delete_video(
        self,
        tv_id: int,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        A valid session or guest session ID is required. You can read more about how this works .

        See more: https://developers.themoviedb.org/3/tv/rate-tv-show
        '''

        def init_session_type(**kwargs):
            return self.request_data(
                request_operation = DeleteRequest(),
                path = f"/tv/{tv_id}/rating",
                headers=url_header_encoded,
                **kwargs)

        if self.type_session == "guest_session":
            parse_data = init_session_type(guest_session_id = self.session_id)

        else:
            parse_data = init_session_type(session_id = self.session_id)


        return datatype.to_datatype(
            parse_data = parse_data,
            model_data = TvVideos)

    def get_latest(
        self,
        datatype : Datatype = ModelDatatype()) -> Any:
        '''
        Get the most newly created TV show. This is a live response and will continuously change.

        See more: https://developers.themoviedb.org/3/tv/get-latest-tv
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/tv/latest")


        return datatype.to_datatype(parse_data = parse_data, model_data = Tv)

    def get_airing_today(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of TV shows that are airing today. This query is purely
        day based as we do not currently support airing times.

        You can specify a  to offset the day calculation. Without a specified timezone,
        this query defaults to EST (Eastern Time UTC-05:00).

        See more: https://developers.themoviedb.org/3/tv/get-latest-tv
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/tv/airing_today",
            page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvAiring)

    def get_on_air(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of shows that are currently on the air.

        This query looks for any TV show that has an episode with an air date in the next 7 days.

        See more: https://developers.themoviedb.org/3/tv/get-tv-on-the-air
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/tv/on_the_air",
            page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvAiring)

    def get_popular(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of the current popular TV shows on TMDB. This list updates daily.

        See more: https://developers.themoviedb.org/3/tv/get-tv-on-the-air
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/tv/popular",
            page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvAiring)

    def get_top_rated(
        self,
        datatype : Datatype = ModelDatatype(),
        page: int = 1) -> Any:
        '''
        Get a list of the top rated TV shows on TMDB.

        See more: https://developers.themoviedb.org/3/tv/get-tv-on-the-air
        '''

        parse_data = self.request_data(
            request_operation = GetRequest(),
            path = "/tv/top_rated",
            page = page)


        return datatype.to_datatype(parse_data = parse_data, model_data = TvAiring)
