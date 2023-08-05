from .task_models import Task


class Track:
    GENERIC = 'generic'
    LINEAR_PROBING = 'linear_probing'
    ZERO_SHOT = 'zero_shot'
    FEW_SHOT = 'few_shot'

    VALID_TYPES = [GENERIC, LINEAR_PROBING, ZERO_SHOT, FEW_SHOT]

    @staticmethod
    def is_valid(task, track):
        if track not in Track.VALID_TYPES:
            return False

        if task in [Task.IC_MULTICLASS, Task.IC_MULTILABEL]:
            return True

        if task in [Task.OD, Task.IMCAP, Task.IMAGE_TEXT_MATCHING, Task.IMAGE_MATTING, Task.IMAGE_TEXT_RETRIEVAL]:
            return track != Track.LINEAR_PROBING

        return False
