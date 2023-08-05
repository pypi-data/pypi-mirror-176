from typing import Any
from dacite import from_dict


class ParseData(dict):
    '''
    Transform Dictionary into dataclass
    '''

    def to_data(self, class_type : Any) -> Any:
        return from_dict(data_class = class_type, data = self)