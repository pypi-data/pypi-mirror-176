from typing import Dict, Union

from .client import Client
from ..models import ModelInfoSubmission


class ModelClient(Client):
    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)
        self._endpoint = f'{self._endpoint}/models'

    def submit_model(self, model_info: Union[ModelInfoSubmission, Dict]):
        assert isinstance(model_info, Dict) or isinstance(model_info, ModelInfoSubmission)
        if isinstance(model_info, Dict):
            model_info = ModelInfoSubmission.from_dict(model_info)
        r = self.post(json=model_info)
        return r
