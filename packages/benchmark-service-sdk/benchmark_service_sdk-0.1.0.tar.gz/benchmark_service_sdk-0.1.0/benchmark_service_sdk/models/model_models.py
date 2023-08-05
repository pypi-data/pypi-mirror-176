import dataclasses
import datetime

from .data_class_base import DataClassBase


@dataclasses.dataclass(frozen=True)
class ModelInfoSubmission(DataClassBase):
    name: str
    token: str
    num_params_in_millions: int
    pretrained_data: str
    creation_time: str

    def validate(self):
        self._check_value('name', lambda x: x)
        self._check_value('token', lambda x: x)
        self._check_value('num_params_in_millions', lambda x: x > 0)
        self._check_value('pretrained_data', lambda x: x)
        self._check_value('creation_time', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
