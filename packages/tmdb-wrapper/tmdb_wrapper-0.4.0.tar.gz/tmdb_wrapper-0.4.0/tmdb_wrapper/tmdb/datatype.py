from abc import ABC, abstractmethod
from typing import Any, Dict

from tmdb_wrapper.tmdb.parse import ParseData

from pprint import pprint

class Datatype(ABC):
    '''
    Abstract Class to get different requests
    '''
    @abstractmethod
    def to_datatype(self, parse_data : ParseData = None, model_data : Any = None):
        pass

class ModelDatatype(Datatype):
    def to_datatype(self,  parse_data : ParseData = None, model_data : Any = None ) -> Any:
        return parse_data.to_data(class_type = model_data)

class DictionaryDatatype(Datatype):
    def to_datatype(self, parse_data : ParseData = None, model_data : Any = None) -> Dict:
        return dict(parse_data)

class PrettifyDatatype(Datatype):
    def to_datatype(self, parse_data : ParseData = None, model_data : Any = None) -> Dict:
        pprint(dict(parse_data))

class OriginalDatatype(Datatype):
    def to_datatype(self, parse_data : ParseData = None, model_data : Any = None) -> Dict:
        return parse_data
