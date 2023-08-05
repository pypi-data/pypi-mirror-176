class Task:
    IC_MULTILABEL = 'classification_multilabel'
    IC_MULTICLASS = 'classification_multiclass'
    OD = 'object_detection'
    IMAGE_TEXT_MATCHING = 'image_text_matching'
    IMCAP = 'image_caption'
    IMAGE_MATTING = 'image_matting'
    IMAGE_TEXT_RETRIEVAL = 'image_text_retrieval'
    VALID_TYPES = [IC_MULTILABEL, IC_MULTICLASS, OD, IMAGE_TEXT_MATCHING, IMCAP, IMAGE_MATTING, IMAGE_TEXT_RETRIEVAL]

    @staticmethod
    def is_classification(dataset_type):
        return dataset_type.startswith('classification')

    @staticmethod
    def is_valid(task):
        return task in Task.VALID_TYPES
