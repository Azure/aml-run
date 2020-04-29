import os
import sys
import importlib
import jsonschema

from azureml.core import RunConfiguration, ScriptRunConfig
from azureml.pipeline.core import Pipeline


class AMLConfigurationException(Exception):
    pass


class AMLExperimentConfigurationException(Exception):
    pass


def convert_to_markdown(metrics_dict):
    exp = list(metrics_dict.keys())

    experiment = exp[0]
    runs = exp

    # add comment header
    markdown = f"## Run Details:%0A%0A Top Level ID: {experiment} %0A%0A"

    # build table header
    markdown += "| Run ID | Parameter | Value |%0A| ----- | ----- | ----- |%0A"
    for run in runs:
        # add metrics and values
        for k, val in metrics_dict[run].items():
            if "best_child_by_primary_metric" in k:
                continue
            row = f"| {run} | {k} |"
            try:
                val = float(val)
                row += f" {val:.3} |"
            except ValueError:
                row += f" {val} |"
            except TypeError:
                row += f" {val} |"
            markdown += row + "%0A"

    return markdown


def mask_parameter(parameter):
    print(f"::add-mask::{parameter}")


def validate_json(data, schema, input_name):
    validator = jsonschema.Draft7Validator(schema)
    errors = validator.iter_errors(data)
    if len(list(errors)) > 0:
        for error in errors:
            print(f"::error::JSON validation error: {error}")
        raise AMLConfigurationException(f"JSON validation error for '{input_name}'. Provided object does not match schema. Please check the output for more details.")
    else:
        print(f"::debug::JSON validation passed for '{input_name}'. Provided object does match schema.")


def load_pipeline_yaml(workspace, pipeline_yaml_file):
    try:
        run_config = Pipeline.load_yaml(
            workspace=workspace,
            filename=pipeline_yaml_file
        )
    except Exception as exception:
        print(f"::debug::Error when loading pipeline yaml definition your repository (Path: /{pipeline_yaml_file}): {exception}")
        run_config = None
    return run_config


def load_runconfig_yaml(runconfig_yaml_file):
    try:
        run_config = RunConfiguration().load(
            path=runconfig_yaml_file
        )

        # Setting source directory for script run config
        source_directory = os.path.split(runconfig_yaml_file)[0]
        source_directory = os.path.split(source_directory)[0] if os.path.split(source_directory)[-1] == ".azureml" or os.path.split(source_directory)[-1] == "aml_config" else source_directory

        # defining scriptrunconfig
        run_config = ScriptRunConfig(
            source_directory=source_directory,
            run_config=run_config
        )
    except TypeError as exception:
        print(f"::debug::Error when loading runconfig yaml definition your repository (Path: /{runconfig_yaml_file}): {exception}")
        run_config = None
    except FileNotFoundError as exception:
        print(f"::debug::Error when loading runconfig yaml definition your repository (Path: /{runconfig_yaml_file}): {exception}")
        run_config = None
    return run_config


def load_runconfig_python(workspace, runconfig_python_file, runconfig_python_function_name):
    root = os.environ.get("GITHUB_WORKSPACE", default=None)

    print("::debug::Adding root to system path")
    sys.path.insert(1, f"{root}")

    print("::debug::Importing module")
    runconfig_python_file = f"{runconfig_python_file}.py" if not runconfig_python_file.endswith(".py") else runconfig_python_file
    try:
        run_config_spec = importlib.util.spec_from_file_location(
            name="runmodule",
            location=runconfig_python_file
        )
        run_config_module = importlib.util.module_from_spec(spec=run_config_spec)
        run_config_spec.loader.exec_module(run_config_module)
        run_config_function = getattr(run_config_module, runconfig_python_function_name, None)
    except ModuleNotFoundError as exception:
        print(f"::debug::Could not load python script in your repository which defines the experiment config (Script: /{runconfig_python_file}, Function: {runconfig_python_function_name}()): {exception}")
    except FileNotFoundError as exception:
        print(f"::debug::Could not load python script or function in your repository which defines the experiment config (Script: /{runconfig_python_file}, Function: {runconfig_python_function_name}()): {exception}")
    except AttributeError as exception:
        print(f"::debug::Could not load python script or function in your repository which defines the experiment config (Script: /{runconfig_python_file}, Function: {runconfig_python_function_name}()): {exception}")

    # Load experiment config
    print("::debug::Loading experiment config")
    try:
        run_config = run_config_function(workspace)
    except TypeError as exception:
        print(f"::error::Could not load experiment config from your module (Script: /{runconfig_python_file}, Function: {runconfig_python_function_name}()): {exception}")
        run_config = None
    return run_config



