import dataclasses
import math
from typing import List, Optional

from .data_class_base import DataClassBase
from .task_models import Task
from .track_models import Track


@dataclasses.dataclass(frozen=True)
class PredictionSubmission(DataClassBase):
    '''Prediction submission class
    Args:
        dataset_name: name of the dataset used to generate the prediction
        model_name: name of the model that predicts the result
        task_name: name of the task
        track_name: name of the track
        predictions: list of predictions
        dataset_version: version of the dataset
        rnd_seeds: random seeds used to generate the predictions
        n_shot: number of instances used in few shot setting
        num_trainable_params_in_millions: number of trainable params of the model
        extra_info: a dict of extra infomation
        token: token of the target leaderboard, this is required when you want to send the results to a leaderboard
        created_by: owner of this prediction submission
        blob_container: a blob container path to the prediction files for image matting task
    '''

    dataset_name: str
    model_name: str
    task_name: str
    track_name: str
    predictions: List
    dataset_version: Optional[int] = None
    rnd_seeds: Optional[List] = None
    n_shot: Optional[int] = None
    num_trainable_params_in_millions: Optional[int] = None
    extra_info: Optional[dict] = None
    token: Optional[str] = None
    created_by: Optional[str] = None
    blob_container: Optional[str] = None

    def validate(self) -> None:

        self._check_value('dataset_name', lambda x: x)
        self._check_value('model_name', lambda x: x)
        self._check_value('task_name', lambda x: Task.is_valid(x))
        self._check_value('track_name', lambda x: Track.is_valid(self.task_name, x))
        self._check_value('predictions', lambda x: x)
        self._check_value('predictions', lambda x: len(set([len(p) for p in x])) == 1, 'lengths of prediction sets of different rnd seeds are not the same.')
        self._check_value('num_trainable_params_in_millions', lambda x: x > 0)

        if self.track_name == Track.FEW_SHOT:
            self._check_value('n_shot', lambda x: x and x > 0)

        if self.rnd_seeds is not None and len(self.rnd_seeds) != len(self.predictions):
            raise ValueError(f'length of rnd_seeds and predictions should be the same, {len(self.rnd_seeds)} vs {len(self.predictions)}')

        if self.dataset_version is not None:
            self._check_value('dataset_version', lambda x: x >= 0)

        for fold_idx, predictions in enumerate(self.predictions):
            PredictionSubmission.validate_predictions(predictions, fold_idx, self.task_name)

    @staticmethod
    def validate_predictions(predictions, fold_idx, task_name):
        assert predictions, f'fold {fold_idx}, empty predictions.'

        if task_name in [Task.IC_MULTICLASS, Task.IC_MULTILABEL]:
            for i, probs in enumerate(predictions):
                if task_name == Task.IC_MULTICLASS:
                    sum_probs = sum(probs)
                    assert math.isclose(sum_probs, 1.0, rel_tol=1e-3), f'fold {fold_idx}, sum of predicted prob vector for image {i}: {sum_probs}, should be 1.0.'

                assert all([0.0 <= prob <= 1.0 for prob in probs]), f'fold {fold_idx}, predicted prob for image {i} not in [0, 1]: {probs}'

        if task_name == Task.OD:
            # [[[class_index, conf, L, T, R, B], [class_index, conf, L, T, R, B], ..., []], [...], ..., [...]]
            for i, img_wise_bboxes in enumerate(predictions):
                for bbox_pred in img_wise_bboxes:
                    assert PredictionSubmission.is_valid_box(bbox_pred), f'fold {fold_idx}, invalid predicted bbox for image {i}: {bbox_pred}'

        if task_name == Task.IMAGE_TEXT_RETRIEVAL:
            assert len(predictions) == 2, f'fold {fold_idx}, invalid predictions for, expected two matrices, got {len(predictions)}'

    @staticmethod
    def is_valid_box(bbox_pred):
        return len(bbox_pred) == 6 and (0.0 <= bbox_pred[1] <= 1.0) and all([x >= 0 for x in bbox_pred[2:]]) and (bbox_pred[2] <= bbox_pred[4]) \
            and (bbox_pred[3] <= bbox_pred[5])
