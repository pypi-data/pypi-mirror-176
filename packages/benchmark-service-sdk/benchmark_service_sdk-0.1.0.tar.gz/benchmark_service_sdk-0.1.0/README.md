# Benchmark Service SDK

## Introduction

Benchmark Service is a tool to handle benchmark request. The tool will collect submitted predictions and ground truth and call vision_evaluation ([link](https://github.com/microsoft/vision-evaluation)) to compute the results. 

This repo provides a python SDK for the Benchmark Service APIs. Specifically, three major APIs are supported now in this SDK:

- submit model information
- submit predictions
- get job status

## Submit model information

To submit the model information, you need to prepare the name of your azure function.

Here is an example of the model json format:

The following script shows an example of how to utilize the SDK to submit the model information.

```python
from benchmark_service_sdk import ModelClient, ModelInfoSubmission

# define your azure function name here
azure_function_name = <your_azure_function_name>
# define a model client
model_client = ModelClient(azure_function_name)
# define a ModelInfoSubmission instance
model_info = ModelInfoSubmission(name="<your model name>",
                                 token="<your MSA/AAD token>",
                                 num_params_in_millions="<params number of your model>",
                                 pretrained_data="<pretrained dataset>",
                                 creation_time="<model creation time>")

# submit your model info to azure function
model_client.submit_model(model_info)
```
Another way to define a `ModelInfoSubmission` instance is using the from_dict function of `ModelInfoSubmission`, e.g.
```python
model_info_json = {"name": "name of a model",
                   "token": "a MSA/AAD token acquired after registration on benchmark UX.",
                   "num_params_in_millions": 320,
                   "pretrained_data": "coco",
                   "creation_time": "2022-09-17"}
model_info = ModelInfoSubmission.from_dict(model_info_json)

# submit your model info to azure function
model_client.submit_model(model_info)
```

## Submit predictions
To submit the prediction results, you will need to prepare the name of your azure function. Here is an example of how to utilize the SDK to submit the predictions.

```python
from benchmark_service_sdk import PredictionClient, PredictionSubmission

# define your azure function name here
azure_function_name = <your_azure_function_name>
# define a prediction client
prediction_client = PredictionClient(azure_function_name)
prediction_info = PredictionSubmission(model_name="<your_model_name>",
                                       dataset_name="<dataset_name>",
                                       track_name="<track_name>",
                                       task_name="<task_name>",
                                       predictions=<predictions to submit>,
                                       dataset_version=<dataset_version>,
                                       rnd_seeds=<random_seed, optional>,
                                       num_trainable_params_in_millions=<model params number, optional>,
                                       extra_info=<etrac_info, optional>,
                                       token="<token, optional>",
                                       created_by="<owner of this submission, optional>")

prediction_client.submit_prediction(prediction_info)
# you can also submit a prediction with a url link to a prediction json file
prediction_json_url = <your prediction json url>
prediction_client.submit_prediction_url(prediction_url=prediction_json_url)
```

Similar to `ModelInfoSubmission`, you can also create a `PredictionSubmission` instance from a dictionay object, here is an example:

```json
{
    "model_name": "name of a model",
    "dataset_name": "coco",
    "track_name": "linear_probing", 
    "task_name": "classification_multiclass",
    "predictions": [predictions_set1, predictions_set2, predictions_setn],
    "rnd_seeds": [rnd_seed1, rnd_seed2, rnd_seed3],
    "dataset_version": 1,
    "num_trainable_params_in_millions": 10,
    "n_shot": 1, // only needed in few_shot track
    "extra_info": {},
    "token": "a MSA/AAD token acquired after registration on benchmark UX.",
    "created_by": "owner's name"
}
```

For the `track_name`, the candidates are: ['generic', 'linear_probing', 'zero_shot', 'few_shot']

For the `task_name`, the candidates are: ['classification_multilabel', 'classification_multiclass', 'object_detection', 'image_text_matching', 'image_caption', 'image_matting', 'image_text_retrieval'] 

For the `predictions`, it is a set of predictions corresponding to different random seeds. For each set, it is a list of predictions for each image, in the order same as the order of images read from the test set. 

- **Image Classification**: A prob vector, the length of which is the number of classes, e.g., [0.1, 0.3, 0.6] for multiclass, [0.3, 0.6, 0.2] for multilabel
- **Object Detection**: A list of bboxes, `[[class_index, confidence, L, T, R, B], [class_index, confidence, L, T, R, B], ..., []]`. Note that class index always starts from zero and box is with absolute coordinates.
- **Image Captioning**: A predicted caption, e.g. `A dog sitting outside.`.
- **Image Text Matching**: Image text matching is slightly different, for each set of predictions, it is a single vector, each element of which is a probabilistic conf indicating whether (image, text) matches, e.g., `[img_1_text_1_match_conf, img_1_text_2_match_conf, img_2_text_1_match_conf, ...]`.
- **Image Text Retrieval**: The predictions include two parts. The first part is an image-to-text retrieval top-k indices matrix, the second part is a text-to-image top-k indices retrieval matrix.
- **Image Matting**: For image matting, the element in each prediction set is a path to a file relative to the URL, and a SAS/blob container should be provided in the json under blob_container.

Example:
```json
{
    "model_name": "a model",
    "dataset_name": "matting_dataset",
    "track": "zero_shot",
    "task": "image_matting",
    "token": "your MSA/AAD token acquired after registration on benchmark UX.",
    "blob_container": "your blob container (sas)",
    "predictions": [
      ["preds/image_1_matting.png", "preds/image_2_matting.png", ...], // prediction set 1
      [...],
      ...]
}
```



## Get job status

Sometimes we need to get the status of a job that we just submitted. To get the job status, you need to prepare:

- a valid job ID
- your azure function name

Here is an example of how to get the job status with a job ID:

```python
from benchmark_service_sdk import JobClient

# define your azure function name here
azure_function_name = <your_azure_function_name>
job_id = <your_job_id>
# define a job client
job_client = JobClient(azure_function_name)

# get the status of the job
r = job_client.query_job_status(job_id=job_id)
```