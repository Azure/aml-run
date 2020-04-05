![Integration Test](https://github.com/Azure/aml-run/workflows/Integration%20Test/badge.svg)
![Lint](https://github.com/Azure/aml-run/workflows/Lint/badge.svg)

# Azure Machine Learning Run Action

## Usage

The Azure Machine Learning Run action will allow you to submit a run (Estimator, ML Pipeline, ScriptRunConfig or AutoMLConfig) to your Azure Machine Learning Workspace. To submit a run, you have to define
1. Your python file(s) that should run remotely and
2.
    a) Either a python script (default `code/train/run_config.py`) which includes a function (default ` def main(workspace):`) that describes your run that you want to submit. The python script gets the [workspace object](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace(class)?view=azure-ml-py) injected and has to return one of the following objects:
    - [Estimator](https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.estimator.estimator?view=azure-ml-py)
    - [TensorFlow Estimator](https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.dnn.tensorflow?view=azure-ml-py)
    - [PyTorch Estimator](https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.dnn.pytorch?view=azure-ml-py)
    - [Scikit Learn Estimator](https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.sklearn.sklearn?view=azure-ml-py)
    - [Chainer Estimator](https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.dnn.chainer?view=azure-ml-py)
    - [Pipeline](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipeline%28class%29?view=azure-ml-py) or
    - [AutoMLConfig](https://docs.microsoft.com/en-us/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig?view=azure-ml-py)
    
    If you want to change the default values for the python script, you can specify it with the `run_config_file_path` and `run_config_file_function_name` parameters.
    
    b) or a Pipeline YAML file (default `"code/train/pipeline.yml"`), which describes your Azure Machine Learning Pipeline that you want to submit. You can change the default value with the `pipeline_yaml_file` parameter.

This action requires an AML workspace to be created or attached to via the [aml-workspace](https://github.com/Azure/aml-workspace) action and some compute resources to be available, which can be managed via the [aml-compute](https://github.com/Azure/aml-compute) action.

## Template repositories

This action is one in a series of actions that can be used to setup an ML Ops process. Examples of these can be found at
1. Simple example: [ml-template-azure](https://github.com/machine-learning-apps/ml-template-azure) and
2. Comprehensive example: [aml-template](https://github.com/Azure/aml-template).

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - name: Check Out Repository
      id: checkout_repository
      uses: actions/checkout@v2

    # AML Workspace Action
    - uses: Azure/aml-workspace
      id: aml_workspace
      with:
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS }}

    # AML Run Action
    - uses: Azure/aml-run
      id: aml_run
      with:
        # required inputs as secrets
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS }}
        # optional
        parameters_file: "run.json"
```

### Inputs

| Input | Required | Default | Description |
| ----- | -------- | ------- | ----------- |
| azure_credentials | x | - | Output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth`. This should be stored in your secrets |
| parameters_file |  | `"compute.json"` | JSON file in the `.cloud/.azure` folder specifying your Azure Machine Learning compute target details. |

#### Azure Credentials

Azure credentials are required to connect to your Azure Machine Learning Workspace. These may have been created for an action you are already using in your repository, if so, you can skip the steps below.

Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your computer or use the Cloud CLI and execute the following command to generate the required credentials:

```sh
# Replace {service-principal-name}, {subscription-id} and {resource-group} with your Azure subscription id and resource group name and any name for your service principle
az ad sp create-for-rbac --name {service-principal-name} \
                         --role contributor \
                         --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                         --sdk-auth
```

This will generate the following JSON output:

```sh
{
  "clientId": "<GUID>",
  "clientSecret": "<GUID>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>",
  (...)
}
```

Add this JSON output as [a secret](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets) with the name `AZURE_CREDENTIALS` in your GitHub repository.

#### Parameter File

The action tries to load a JSON file in the `.cloud/.azure` folder in your repository, which specifies details of your Azure Machine Learning Run. By default, the action is looking for a file with the name `"run.json"`. If your JSON file has a different name, you can specify it with this parameter. Note that none of these values are required and in the absence, defaults will be created with a combination of the repo name and branch name.

A sample file can be found in this repository in the folder `.cloud/.azure`. The JSON file can include the following parameters:

| Parameter Name        | Required | Allowed Values           | Default    | Description |
| --------------------- | -------- | ------------------------ | ---------- | ----------- |
| experiment_name       |          | str                      | <REPOSITORY_NAME>-<BRANCH_NAME> | Name of your experiment in AML, which must be 3-36 characters, start with a letter or a number, and can only contain letters, numbers, underscores, and dashes. |
| run_config_file_path  |          | str                      | `"code/train/run_config.py"`      | Path to the python script in your repository  in which you define your run and return an Estimator, Pipeline, AutoMLConfig or ScriptRunConfig object. |
| run_config_file_function_name |          | str                      | `"main"`              | Name of the function in your python script in your repository in which you define your run and return an Estimator, Pipeline, AutoMLConfig or ScriptRunConfig object. The function gets the workspace object passed as an argument. |
| tags                  |          | dict: {"<your-run-tag-key>": "<your-run-tag-value>", ...}  | null       | Tags to be added to the submitted run. |
| wait_for_completion   |          | bool                     | true                  | Indicates whether the action will wait for completion of the run |
| pipeline_yaml_file         |          | str                      | `"code/train/pipeline.yml"`      | Name of your pipeline YAML file. |
| pipeline_publish      |          | bool: true, false        | false                 | Indicates whether the action will publish the pipeline after submitting it to Azure Machine Learning. This only works if you submitted a pipeline. |
| pipeline_name         |          | str                      | <REPOSITORY_NAME>-<BRANCH_NAME> | The name of the published pipeline. |
| pipeline_version      |          | str                      | null                  | The version of the published pipeline. |
| pipeline_continue_on_step_failure |  | bool                | false                 | Whether to continue execution of other steps in the PipelineRun if a step fails. |

### Outputs

| Output                         | Description                                   |
| ------------------------------ | --------------------------------------------- |
| experiment_name              | Name of the experiment of the run             |
| run_id                       | ID of the run                                 |
| run_url                      | URL to the run in the Azure Machine Learning Studio    |
| run_metrics                  | Metrics of the run (will only be provided if wait_for_completion is set to True)    |
| published_pipeline_id        | Id of the published pipeline (will only be provided if you submitted a pipeline and pipeline_publish is set to True) |
| published_pipeline_status    | Status of the published pipeline (will only be provided if you submitted a pipeline and pipeline_publish is set to True) |
| published_pipeline_endpoint  | Endpoint of the published pipeline (will only be provided if you submitted a pipeline and pipeline_publish is set to True) |

### Other Azure Machine Learning Actions

- [aml-workspace](https://github.com/Azure/aml-workspace) - Connects to or creates a new workspace
- [aml-compute](https://github.com/Azure/aml-compute) - Connects to or creates a new compute target in Azure Machine Learning
- [aml-run](https://github.com/Azure/aml-run) - Submits a ScriptRun, an Estimator or a Pipeline to Azure Machine Learning
- [aml-registermodel](https://github.com/Azure/aml-registermodel) - Registers a model to Azure Machine Learning
- [aml-deploy](https://github.com/Azure/aml-deploy) - Deploys a model and creates an endpoint for the model

### Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
