![Integration Test](https://github.com/Azure/aml-run/workflows/Integration%20Test/badge.svg)
![Lint](https://github.com/Azure/aml-run/workflows/Lint/badge.svg)

# Azure Machine Learning Run Action

## Usage

The Azure Machine Learning Run action will allow you to run an experiment run or a training pipeline on Azure Machine Learning.

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

#### Parameter File

A sample file can be found in this repository in the folder `.aml`. The action expects a similar parameter file in your repository in the `.aml folder`.

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
