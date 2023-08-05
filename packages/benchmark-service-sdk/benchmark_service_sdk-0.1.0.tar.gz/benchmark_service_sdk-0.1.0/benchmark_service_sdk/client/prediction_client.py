from typing import Dict, Union
from .client import Client
from ..models import PredictionSubmission


class PredictionClient(Client):
    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)
        self._endpoint = f'{self._endpoint}/predictions'

    def submit_prediction(self, prediction_submission: Union[PredictionSubmission, Dict]):
        assert isinstance(prediction_submission, Dict) or isinstance(prediction_submission, PredictionSubmission)
        if isinstance(prediction_submission, Dict):
            prediction_submission = PredictionSubmission.from_dict(prediction_submission)
        r = self.post(json=prediction_submission)
        return r

    def submit_prediction_url(self, prediction_url: str):
        if not (prediction_url.startswith('https://') or prediction_url.startswith('http://')):
            raise ValueError(f'{prediction_url} is not a valid url!')
        r = self.post(params={'json_url': prediction_url})
        return r
