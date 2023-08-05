import unittest
from copy import deepcopy

from benchmark_service_sdk import ModelInfoSubmission, Task, Track, PredictionSubmission


class TestModelInfoSubmission(unittest.TestCase):
    dummy_model_info = {'name': 'dummy_model',
                        'token': 'dummy_token',
                        'num_params_in_millions': 1,
                        'pretrained_data': 'dummy_dataset',
                        'creation_time': '2022-11-01'}

    def test_model_info_submission(self):
        model_info = ModelInfoSubmission.from_dict(self.dummy_model_info)
        self.assertDictEqual(self.dummy_model_info, model_info.to_dict())

    def test_wrong_creation_time_raise_value_error(self):
        model_info = deepcopy(self.dummy_model_info)
        model_info['creation_time'] = '2022-11-0'
        with self.assertRaises(ValueError):
            ModelInfoSubmission.from_dict(model_info)

    def test_missing_required_key_raise_type_error(self):
        for key in self.dummy_model_info:
            model_info = deepcopy(self.dummy_model_info)
            model_info.pop(key)
            with self.assertRaises(TypeError):
                ModelInfoSubmission.from_dict(model_info)

    def test_extra_key_raise_assertation_error(self):
        model_info = deepcopy(self.dummy_model_info)
        model_info['extra_key'] = 'extra_value'
        with self.assertRaises(AssertionError):
            ModelInfoSubmission.from_dict(model_info)


class TestPredictionSubmission(unittest.TestCase):
    dummy_prediction = {"model_name": "dummy_model",
                        "dataset_name": "mock_dataset_multiclass_ic",
                        "track_name": "zero_shot",
                        "task_name": Task.IC_MULTICLASS,
                        "predictions": [[[0.1, 0.9], [0.2, 0.8]]],
                        "rnd_seeds": [0],
                        "num_trainable_params_in_millions": 10,
                        "dataset_version": 1,
                        "token": "dummy_token",
                        "extra_info": {},
                        "created_by": "dummy_creator"}

    def test_prediction_submission(self):
        prediction_submission = PredictionSubmission.from_dict(self.dummy_prediction)
        self.assertDictEqual(self.dummy_prediction, prediction_submission.to_dict())

    def test_missing_required_key_raise_type_error(self):
        for key in ["model_name", "dataset_name", "track_name", "task_name", "predictions"]:
            prediction = deepcopy(self.dummy_prediction)
            prediction.pop(key)
            with self.assertRaises(TypeError):
                PredictionSubmission.from_dict(prediction)

    def test_extra_key_raise_assertation_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['extra_key'] = 'extra_value'
        with self.assertRaises(AssertionError):
            PredictionSubmission.from_dict(prediction)

    def test_invalid_track_name_raise_value_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['track_name'] = 'dummy_track'
        with self.assertRaises(ValueError):
            PredictionSubmission.from_dict(prediction)

    def test_invalid_task_name_raise_value_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['task_name'] = 'dummy_task'
        with self.assertRaises(ValueError):
            PredictionSubmission.from_dict(prediction)

    def test_negative_n_few_shot_raise_value_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['track_name'] = 'few_shot'
        prediction['n_shot'] = -1
        with self.assertRaises(ValueError):
            PredictionSubmission.from_dict(prediction)

    def test_invalid_dataset_version_raise_value_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['dataset_version'] = -1
        with self.assertRaises(ValueError):
            PredictionSubmission.from_dict(prediction)

    def test_random_seed_prediction_len_mismatch_raise_value_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['rnd_seeds'] = [0, 1]
        with self.assertRaises(ValueError):
            PredictionSubmission.from_dict(prediction)

    def test_ic_multiclass_prob_sum_not_one_raise_assertation_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['predictions'] = [[[0.1, 0.2], [0.2, 0.8]]]
        with self.assertRaises(AssertionError):
            PredictionSubmission.from_dict(prediction)

    def test_ic_prob_beyond_zero_and_one_raise_assertation_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['predictions'] = [[[-0.1, 1.1], [0.2, 0.8]]]
        with self.assertRaises(AssertionError):
            PredictionSubmission.from_dict(prediction)

    def test_od_invalid_prediction_raise_assertation_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['task_name'] = Task.OD
        invalid_predictions = []
        # length of bbox is not 6
        invalid_predictions.append([[[[0, 0.8, 10, 10, 20]]]])
        # confidence value beyond [0, 1]
        invalid_predictions.append([[[[0, -0.1, 10, 10, 20, 20]]]])
        invalid_predictions.append([[[[0, 1.1, 10, 10, 20, 20]]]])
        # negative value in LTRB coordinates
        invalid_predictions.append([[[[0, 0.8, -1, 10, 20, 20]]]])
        invalid_predictions.append([[[[0, 0.8, 1, -1, 20, 20]]]])
        invalid_predictions.append([[[[0, 0.8, 1, 1, -20, 20]]]])
        invalid_predictions.append([[[[0, 0.8, 1, 1, 20, -20]]]])
        # left coordinate larger than right
        invalid_predictions.append([[[[0, 0.8, 20, 1, 1, 20]]]])
        # bottom coordinate larger than top
        invalid_predictions.append([[[[0, 0.8, 1, 20, 20, 1]]]])
        for invalid_prediction in invalid_predictions:
            prediction['predictions'] = invalid_prediction
            with self.assertRaises(AssertionError):
                PredictionSubmission.from_dict(prediction)

    def test_image_tex_retrieval_invalid_prediction_len_raise_assertation_error(self):
        prediction = deepcopy(self.dummy_prediction)
        prediction['task_name'] = Task.IMAGE_TEXT_RETRIEVAL
        prediction['predictions'] = [[[2, 1]]]
        with self.assertRaises(AssertionError):
            PredictionSubmission.from_dict(prediction)


class TestTask(unittest.TestCase):
    def test_valid_task(self):
        valid_tasks = Task.VALID_TYPES
        for task in valid_tasks:
            self.assertTrue(Task.is_valid(task))

    def test_invalid_task(self):
        invalid_tasks = ['invalid_dummy_task']
        for task in invalid_tasks:
            self.assertFalse(Task.is_valid(task))


class TestTrack(unittest.TestCase):
    def test_valid_track(self):
        valid_tracks = Track.VALID_TYPES
        valid_tasks = Task.VALID_TYPES

        for track in valid_tracks:
            for task in valid_tasks:
                if Task.is_classification(task):
                    self.assertTrue(Track.is_valid(task, track))
                else:
                    if track == Track.LINEAR_PROBING:
                        self.assertFalse(Track.is_valid(task, track))
                    else:
                        self.assertTrue(Track.is_valid(task, track))

    def test_invalid_track(self):
        invalid_tracks = ['invalid_dummy_track']
        valid_tasks = Task.VALID_TYPES
        for track in invalid_tracks:
            for task in valid_tasks:
                self.assertFalse(Track.is_valid(task, track))
