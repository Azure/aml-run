azure_credentials_schema = {
    "$id": "http://azure-ml.com/schemas/azure_credentials.json",
    "$schema": "http://json-schema.org/schema",
    "title": "azure_credentials",
    "description": "JSON specification for your azure credentials",
    "type": "object",
    "required": ["clientId", "clientSecret", "subscriptionId", "tenantId"],
    "properties": {
        "clientId": {
            "type": "string",
            "description": "The client ID of the service principal."
        },
        "clientSecret": {
            "type": "string",
            "description": "The client secret of the service principal."
        },
        "subscriptionId": {
            "type": "string",
            "description": "The subscription ID that should be used."
        },
        "tenantId": {
            "type": "string",
            "description": "The tenant ID of the service principal."
        }
    }
}

parameters_schema = {
    "$id": "http://azure-ml.com/schemas/compute.json",
    "$schema": "http://json-schema.org/schema",
    "title": "aml-compute",
    "description": "JSON specification for your compute details",
    "type": "object",
    "properties": {
        "experiment_name": {
            "type": "string",
            "description": "The name of your experiment in AML.",
            "minLength": 3,
            "maxLength": 36
        },
        "tags": {
            "type": "object",
            "description": "Tags to be added to the submitted run."
        },
        "wait_for_completion": {
            "type": "boolean",
            "description": "Indicates whether the action will wait for completion of the run."
        },
        "runconfig_python_file": {
            "type": "string",
            "description": "Path to the python script in your repository in which you define your run and return an Estimator, Pipeline, AutoMLConfig or ScriptRunConfig object."
        },
        "runconfig_python_function_name": {
            "type": "string",
            "description": "The name of the function in your python script in your repository in which you define your run and return an Estimator, Pipeline, AutoMLConfig or ScriptRunConfig object. The function gets the workspace object passed as an argument."
        },
        "runconfig_yaml_file": {
            "type": "string",
            "description": "The name of your runconfig YAML file."
        },
        "pipeline_yaml_file": {
            "type": "string",
            "description": "The name of your pipeline YAML file."
        },
        "pipeline_publish": {
            "type": "boolean",
            "description": "Indicates whether the action will publish the pipeline after submitting it to Azure Machine Learning. This only works if you submitted a pipeline."
        },
        "pipeline_name": {
            "type": "string",
            "description": "The name of the published pipeline."
        },
        "pipeline_version": {
            "type": "string",
            "description": "The version of the published pipeline."
        },
        "pipeline_continue_on_step_failure": {
            "type": "boolean",
            "description": "Indicates whether the published pipeline will continue execution of other steps in the PipelineRun if a step fails."
        }
    }
}

markdown_conversion_input = {
    '5815b172-61fe-4e8d-baa2-e4ffe33e77d3': {'testkey': 'testvalue'},
    'HD_7034e363-3172-41e6-8423-eb292f39e233': {
        'best_child_by_primary_metric': {
            'metric_name': ['mse', 'mse'],
            'timestamp': ['2020-04-06 16:04:23.719570+00:00',
                          '2020-04-06 16:04:23.719570+00:00'],
            'run_id': ['HD_7034e363-3172-41e6-8423-eb292f39e233_1',
                       'HD_7034e363-3172-41e6-8423-eb292f39e233_1'],
            'metric_value': [0.025010755222666936, 0.025010755222666936],
            'final': [False, True]}},
    'HD_7034e363-3172-41e6-8423-eb292f39e233_0': {
        'auc': 0.6394267984578837,
        'mse': 0.025010755222666936,
        'TimeSeries comparison': 'aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png'},
    'HD_7034e363-3172-41e6-8423-eb292f39e233_1': {
        'auc': 0.6394267984578837,
        'mse': 0.025010755222666936,
        'TimeSeries comparison': 'aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png'},
    'HD_7034e363-3172-41e6-8423-eb292f39e233_2': {
        'mse': 0.025010755222666936,
        'auc': 0.6394267984578837,
        'TimeSeries comparison': 'aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png'}}

markdown_out = '''## Run Details:%0A%0A Experiment/Pipeline ID: 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 %0A%0A| Run ID | Parameter | Value |%0A| ----- | ----- | ----- |%0A| 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 | testkey | testvalue |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png |%0A'''
