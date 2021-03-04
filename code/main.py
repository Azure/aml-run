import os
import json
import logging

from azureml.core import Workspace, Experiment
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.pipeline.core import PipelineRun
from azureml.train.hyperdrive import HyperDriveRun
from azureml.exceptions import AuthenticationException, ProjectSystemException, AzureMLException, UserErrorException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, AMLExperimentConfigurationException, mask_parameter, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python, validate_json, convert_to_markdown
from schemas import azure_credentials_schema, parameters_schema
from azureml.core.dataset import Dataset
from azureml.train.automl import AutoMLConfig
from azureml.core.compute import ComputeTarget, AmlCompute


def main():
    # Loading azure credentials
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException(
            "Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")

    # Checking provided parameters
    print("::debug::Checking provided parameters")
    validate_json(
        data=azure_credentials,
        schema=azure_credentials_schema,
        input_name="AZURE_CREDENTIALS"
    )

    # Mask values
    print("::debug::Masking parameters")
    mask_parameter(parameter=azure_credentials.get("tenantId", ""))
    mask_parameter(parameter=azure_credentials.get("clientId", ""))
    mask_parameter(parameter=azure_credentials.get("clientSecret", ""))
    mask_parameter(parameter=azure_credentials.get("subscriptionId", ""))

    # Loading parameters file
    print("::debug::Loading parameters file")
    parameters_file = os.environ.get(
        "INPUT_PARAMETERS_FILE", default="run.json")
    parameters_file_path = os.path.join(".cloud", ".azure", parameters_file)
    try:
        with open(parameters_file_path) as f:
            parameters = json.load(f)
    except FileNotFoundError:
        print(
            f"::debug::Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository if you do not want to use default settings (e.g. .cloud/.azure/run.json).")
        parameters = {}

    # Checking provided parameters
    print("::debug::Checking provided parameters")
    validate_json(
        data=parameters,
        schema=parameters_schema,
        input_name="PARAMETERS_FILE"
    )

    # Define target cloud
    if azure_credentials.get("resourceManagerEndpointUrl", "").startswith("https://management.usgovcloudapi.net"):
        cloud = "AzureUSGovernment"
    elif azure_credentials.get("resourceManagerEndpointUrl", "").startswith("https://management.chinacloudapi.cn"):
        cloud = "AzureChinaCloud"
    else:
        cloud = "AzureCloud"

    # Loading Workspace
    print("::debug::Loading AML Workspace")
    sp_auth = ServicePrincipalAuthentication(
        tenant_id=azure_credentials.get("tenantId", ""),
        service_principal_id=azure_credentials.get("clientId", ""),
        service_principal_password=azure_credentials.get("clientSecret", ""),
        cloud=cloud
    )
    config_file_path = os.environ.get(
        "GITHUB_WORKSPACE", default=".cloud/.azure")
    config_file_name = "aml_arm_config.json"
    try:
        ws = Workspace.from_config(
            path=config_file_path,
            _file_name=config_file_name,
            auth=sp_auth
        )
    except AuthenticationException as exception:
        print(
            f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        raise AuthenticationException
    except AuthenticationError as exception:
        print(f"::error::Microsoft REST Authentication Error: {exception}")
        raise AuthenticationError
    except AdalError as exception:
        print(
            f"::error::Active Directory Authentication Library Error: {exception}")
        raise AdalError
    except ProjectSystemException as exception:
        print(f"::error::Workspace authorizationfailed: {exception}")
        raise ProjectSystemException

    # Create experiment
    print("::debug::Creating experiment")
    try:
        # Default experiment name
        repository_name = os.environ.get("GITHUB_REPOSITORY").split("/")[-1]
        branch_name = os.environ.get("GITHUB_REF").split("/")[-1]
        default_experiment_name = f"{repository_name}-{branch_name}"

        experiment = Experiment(
            workspace=ws,
            name=parameters.get("experiment_name",
                                default_experiment_name)[:36]
        )
    except TypeError as exception:
        experiment_name = parameters.get("experiment", None)
        print(
            f"::error::Could not create an experiment with the specified name {experiment_name}: {exception}")
        raise AMLExperimentConfigurationException(
            f"Could not create an experiment with the specified name {experiment_name}: {exception}")
    except UserErrorException as exception:
        experiment_name = parameters.get("experiment", None)
        print(
            f"::error::Could not create an experiment with the specified name {experiment_name}: {exception}")
        raise AMLExperimentConfigurationException(
            f"Could not create an experiment with the specified name {experiment_name}: {exception}")

    # Reading the dataset
    print("::debug::Reading the dataset")
    # ds_workspace = Workspace(
    #     'aeefecca-6f22-4523-93ba-bd49686ea0ce', 'mshack-azureml', 'ms-hack')

    # train = Dataset.get_by_name(ds_workspace, name='HistogramTrain')
    # test = Dataset.get_by_name(ds_workspace, name='HistogramTest')

    datastore = ws.get_default_datastore()

    # upload_src = parameters.get("upload_datastore_src_path", "")
    # upload_target = parameters.get("upload_datastore_target_path", "")

    # if (upload_src and upload_target):
    #     datastore.upload(src_dir=upload_src,
    #                      target_path=upload_target, overwrite=True)

    train = Dataset.Tabular.from_delimited_files(
        (datastore, 'histogram/train.csv'))
    test = Dataset.Tabular.from_delimited_files(
        (datastore, 'histogram/test.csv'))

    label_column_name = 'class'

    # Setting AutoML config
    print("::debug::Setting AutoML config")

    automl_settings = {
        "primary_metric": 'accuracy',
        "verbosity": logging.INFO,
        "enable_stack_ensemble": True
    }
    compute_target = ComputeTarget(ws, 'githubcluster')
    automl_config = AutoMLConfig(task='classification',
                                 debug_log='automl_errors.log',
                                 compute_target=compute_target,
                                 training_data=train,
                                 validation_data=test,
                                 experiment_timeout_hours=.25,
                                 label_column_name=label_column_name,
                                 **automl_settings
                                 )

    # Submit run config
    print("::debug::Submitting experiment config")
    try:
        # Defining default tags
        print("::debug::Defining default tags")
        default_tags = {
            "GITHUB_ACTOR": os.environ.get("GITHUB_ACTOR"),
            "GITHUB_REPOSITORY": os.environ.get("GITHUB_REPOSITORY"),
            "GITHUB_SHA": os.environ.get("GITHUB_SHA"),
            "GITHUB_REF": os.environ.get("GITHUB_REF")
        }

        run = experiment.submit(
            automl_config,
            tags=dict(parameters.get("tags", {}), **default_tags)
        )
    except AzureMLException as exception:
        print(
            f"::error::Could not submit experiment config. Your script passed object of type {type(automl_config)}. Object must be correctly configured and of type e.g. estimator, pipeline, etc.: {exception}")
        raise AMLExperimentConfigurationException(
            f"Could not submit experiment config. Your script passed object of type {type(automl_config)}. Object must be correctly configured and of type e.g. estimator, pipeline, etc.: {exception}")
    except TypeError as exception:
        print(
            f"::error::Could not submit experiment config. Your script passed object of type {type(automl_config)}. Object must be correctly configured and of type e.g. estimator, pipeline, etc.: {exception}")
        raise AMLExperimentConfigurationException(
            f"Could not submit experiment config. Your script passed object of type {type(automl_config)}. Object must be correctly configured and of type e.g. estimator, pipeline, etc.: {exception}")

    # Create outputs
    print("::debug::Creating outputs")
    print(f"::set-output name=experiment_name::{run.experiment.name}")
    print(f"::set-output name=run_id::{run.id}")
    print(f"::set-output name=run_url::{run.get_portal_url()}")

    # Waiting for run to complete
    print("::debug::Waiting for run to complete")
    if parameters.get("wait_for_completion", True):
        run.wait_for_completion(show_output=True)

        # Creating additional outputs of finished run
        run_metrics = run.get_metrics() if type(
            run) is HyperDriveRun else run.get_metrics(recursive=True)
        # run_metrics = run.get_metrics(recursive=True) # Not working atm because HyperDriveRun thrown error
        print(f"::set-output name=run_metrics::{run_metrics}")
        run_metrics_markdown = convert_to_markdown(run_metrics)
        print(
            f"::set-output name=run_metrics_markdown::{run_metrics_markdown}")

        # Download artifacts if enabled
        if parameters.get("download_artifacts", False):
            # Defining artifacts folder
            print("::debug::Defining artifacts folder")
            root_path = os.environ.get("GITHUB_WORKSPACE", default=None)
            folder_name = f"aml_artifacts_{run.id}"
            artifact_path = os.path.join(root_path, folder_name)

            # Downloading artifacts
            print("::debug::Downloading artifacts")
            run.download_files(
                output_directory=os.path.join(artifact_path, "parent"))
            children = run.get_children(recursive=True)
            for i, child in enumerate(children):
                child.download_files(output_directory=os.path.join(
                    artifact_path, f"child_{i}"))

            # Creating additional outputs
            print(f"::set-output name=artifact_path::{artifact_path}")

    # Publishing pipeline
    print("::debug::Publishing pipeline")
    if type(run) is PipelineRun and parameters.get("pipeline_publish", False):
        # Default pipeline name
        repository_name = os.environ.get("GITHUB_REPOSITORY").split("/")[-1]
        branch_name = os.environ.get("GITHUB_REF").split("/")[-1]
        default_pipeline_name = f"{repository_name}-{branch_name}"

        published_pipeline = run.publish_pipeline(
            name=parameters.get("pipeline_name", default_pipeline_name),
            description="Pipeline registered by GitHub Run Action",
            version=parameters.get("pipeline_version", None),
            continue_on_step_failure=parameters.get(
                "pipeline_continue_on_step_failure", False)
        )

        # Creating additional outputs
        print(
            f"::set-output name=published_pipeline_id::{published_pipeline.id}")
        print(
            f"::set-output name=published_pipeline_status::{published_pipeline.status}")
        print(
            f"::set-output name=published_pipeline_endpoint::{published_pipeline.endpoint}")
    elif parameters.get("pipeline_publish", False):
        print("::error::Could not register pipeline because you did not pass a pipeline to the action")

    print("::debug::Successfully finished Azure Machine Learning Train Action")


if __name__ == "__main__":
    main()
