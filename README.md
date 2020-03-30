![Integration Test](https://github.com/Azure/aml-run/workflows/Integration%20Test/badge.svg)
![Lint](https://github.com/Azure/aml-run/workflows/Lint/badge.svg)

# Azure Machine Learning Run Action

## Usage

The Azure Machine Learning Run action will allow you to run an experiment run or a training pipeline on Azure Machine Learning. The action will take the training script passed to it from your repository and use that to run a model training run as an experiment unless a pipeline.yaml file is specified and then a pipeline will be run.

This action requires an AML workspace to be created or attached to via the [aml-workspace](https://github.com/Azure/aml-workspace) action and some compute resources to be available, which can be managed via the [aml-compute](https://github.com/Azure/aml-compute) action.

This action is one in a series of actions that are used to make ML Ops systems. Examples of these can be found at [ml-template-azure](https://github.com/machine-learning-apps/ml-template-azure) and [aml-template](https://github.com/Azure/aml-template). 

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action

      # AML Workspace Action
    - uses: azure/aml-run@master
      # required inputs as secrets
      with:
        azureCredentials: ${{ secrets.AZURE_CREDENTIALS }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `AZURE_CREDENTIALS`  | Output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth`. This should be stored in your secrets    |

#### Azure Credentials

azure credentials are required to manage AML. These may have been created for an action you are already using in your repository, if so, you can skip the steps below. 

Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) and execute the following command to generate the credentials:

```sh
# Replace {service-principal-name}, {subscription-id} and {resource-group} with your Azure subscription id and resource group and any name
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

Add the JSON output as [a secret](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets) with the name `AZURE_CREDENTIALS` in the GitHub repository.

#### Parameter File

A sample file can be found in this repository in the folder `.ml`. The action expects a similar parameter file in your repository in the `.ml/azure` folder. Note that none of these values are required and in the absence, defaults will be created with a combination of the repo name and branch name. 

| Parameter Name      | Required | Allowed Values           | Default    | Description |
| ------------------- | -------- | ------------------------ | ---------- | ----------- |
| experiment          |          | str                      | repo-name+branch_name | The name of your experiment in AML     |
| source_directory    |          | str                      | no default | directory where your python script lives |
| script_name         |          | str                      | false      | Create Workspace if it could not be loaded |
| function_name       |          | str                      | null       | Function used in your run script |
| tags                |          | {"<your-run-tag-key>": "<your-run-tag-value>"}  | null       | |
| wait_for_completion |          | bool: true, false        | false      | whether the action will wait for completion |
| pipeline_yaml       |          | str                      | null       | your pipeline yaml file |
| pipeline_publish    |          | bool: true, false        | null       | publish or not |
| pipeline_name       |          | str                      | null       | pipeline name |
| pipeline_version    |          | str.                     | null       | version |
| pipeline_continue_on_step_failure   |          | bool: true, false.            | null       | |

### Outputs

| Output                                             | Description                                        |
|--------------------------------|-----------------------------------------------|
| `experiment_name`              | Name of the experiment of the run   |
| `run_id`                       | ID of the run                       |
| `run_url`                      | URL to the run in the Azure Machine Learning Studio    |
| `run_metrics`                  | Metrics of the run (will only be provided if wait_for_completion is set to True)    |
| `published_pipeline_id`        | Id of the published pipeline (will only be provided if pipeline_publish is set to True and pipeline_name was provided) |
| `published_pipeline_status`    | Status of the published pipeline (will only be provided if pipeline_publish is set to True and pipeline_name was provided) |
| `published_pipeline_endpoint`  | Endpoint of the published pipeline (will only be provided if pipeline_publish is set to True and pipeline_name was provided) |


### Other Azure Machine Learning Actions

- [aml-workspace](https://github.com/Azure/aml-workspace) - Connects to or creates a new workspace
- [aml-compute](https://github.com/Azure/aml-compute) - Connects to or creates a new compute target in Azure Machine Learning
- [aml-run](https://github.com/Azure/aml-run) - Submits a ScriptRun, an Estimator or a Pipeline to Azure Machine Learning
- [aml-registermodel](https://github.com/Azure/aml-registermodel) - Registers a model to Azure Machine Learning
- [aml-deploy](https://github.com/Azure/aml-deploy) - Deploys a model and creates an endpoint for the model
