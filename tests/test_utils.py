import os
import sys
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import AMLConfigurationException, AMLExperimentConfigurationException, convert_to_markdown, validate_json, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python
from schemas import azure_credentials_schema, parameters_schema, 
from objects import markdown_conversion_input, markdown_out


def test_markdown_single_experiment_conversion():
    """
    Unit test to check the markdown conversion
    """
    markdown_conversion_input = {
        "5815b172-61fe-4e8d-baa2-e4ffe33e77d3": {
            "testkey": "testvalue"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233": {
            "best_child_by_primary_metric": {
                "metric_name": ["mse", "mse"],
                "timestamp": ["2020-04-06 16:04:23.719570+00:00", "2020-04-06 16:04:23.719570+00:00"],
                "run_id": ["HD_7034e363-3172-41e6-8423-eb292f39e233_1", "HD_7034e363-3172-41e6-8423-eb292f39e233_1"],
                "metric_value": [0.025010755222666936, 0.025010755222666936],
                "final": [False, True]
            }
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_0": {
            "auc": 0.6394267984578837,
            "mse": 0.025010755222666936,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_1": {
            "auc": 0.6394267984578837,
            "mse": 0.025010755222666936,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_2": {
            "mse": 0.025010755222666936,
            "auc": 0.6394267984578837,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png"
        }
    }
    markdown = convert_to_markdown(
        markdown_conversion_input
    )
    assert markdown == markdown_out


def test_validate_json_valid_inputs():
    """
    Unit test to check the validate_json function with valid inputs
    """
    json_object = {
        "clientId": "",
        "clientSecret": "",
        "subscriptionId": "",
        "tenantId": ""
    }
    schema_path = os.path.join("code", "schemas", "azure_credential_schema.json")
    schema_object = azure_credentials_schema
    validate_json(
        data=json_object,
        schema=schema_object,
        input_name="PARAMETERS_FILE"
    )


def test_validate_json_invalid_json():
    """
    Unit test to check the validate_json function with invalid json_object input
    """
    json_object = {
        "clientId": "",
        "clientSecret": "",
        "subscriptionId": ""
    }
    schema_object = azure_credentials_schema
    with pytest.raises(AMLConfigurationException):
        assert validate_json(
            data=json_object,
            schema=schema_object,
            input_name="PARAMETERS_FILE"
        )


def test_validate_json_invalid_schema():
    """
    Unit test to check the validate_json function with invalid schema input
    """
    json_object = {}
    schema_object = {}
    with pytest.raises(Exception):
        assert validate_json(
            data=json_object,
            schema=schema_object,
            input_name="PARAMETERS_FILE"
        )


def test_load_pipeline_yaml_invalid_inputs():
    """
    Unit test to check the load_pipeline_yaml function with invalid inputs
    """
    workspace = object()
    pipeline_yaml_file = "invalid.yml"
    run_config = load_pipeline_yaml(
        workspace=workspace,
        pipeline_yaml_file=pipeline_yaml_file
    )
    assert run_config == None


def test_load_runconfig_yaml_invalid_yml_file():
    """
    Unit test to check the load_runconfig_yaml function with invalid inputs
    """
    runconfig_yaml_file = "invalid.yml"
    run_config = load_runconfig_yaml(
        runconfig_yaml_file=runconfig_yaml_file
    )
    assert run_config == None


def test_load_runconfig_python_invalid():
    """
    Unit test to check the load_runconfig_python function with invalid inputs
    """
    workspace = object()
    runconfig_python_file = "invalid.py"
    runconfig_python_function_name = ""
    run_config = load_runconfig_python(
        workspace=workspace,
        runconfig_python_file=runconfig_python_file,
        runconfig_python_function_name=runconfig_python_function_name
    )
    assert run_config == None
