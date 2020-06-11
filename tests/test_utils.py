import os
import sys
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import AMLConfigurationException, convert_to_markdown, validate_json, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python
from schemas import azure_credentials_schema
from objects import markdown_conversion_input_1, markdown_conversion_output_1, markdown_conversion_input_2, markdown_conversion_output_2, markdown_conversion_input_3, markdown_conversion_output_3, markdown_conversion_input_4, markdown_conversion_output_4


def test_markdown_single_experiment_conversion():
    """
    Unit test to check the markdown conversion
    """
    markdown_1 = convert_to_markdown(
        metrics_dict=markdown_conversion_input_1
    )
    print(markdown_1)
    assert markdown_1 == markdown_conversion_output_1

    markdown_2 = convert_to_markdown(
        metrics_dict=markdown_conversion_input_2
    )
    print(markdown_2)
    assert markdown_2 == markdown_conversion_output_2

    markdown_3 = convert_to_markdown(
        metrics_dict=markdown_conversion_input_3
    )
    print(markdown_3)
    assert markdown_3 == markdown_conversion_output_3

    markdown_4 = convert_to_markdown(
        metrics_dict=markdown_conversion_input_4
    )
    print(markdown_4)
    assert markdown_4 == markdown_conversion_output_4


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
    assert run_config is None


def test_load_runconfig_yaml_invalid_yml_file():
    """
    Unit test to check the load_runconfig_yaml function with invalid inputs
    """
    runconfig_yaml_file = "invalid.yml"
    run_config = load_runconfig_yaml(
        runconfig_yaml_file=runconfig_yaml_file
    )
    assert run_config is None


def test_load_runconfig_python_invalid_python_file():
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
    assert run_config is None
