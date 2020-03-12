# Azure Machine Learning Run Action



## Usage

Description.

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

    steps:
    - uses: actions/checkout@master
    - name: Run action

      # Put your action repo here
      uses: me/myaction@master

      # Put an example of your mandatory inputs here
      with:
        myInput: world
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

#### Parameter File

A sample file can be found in this repository in the folder `.aml`. The action expects a similar parameter file in your repository in the `.aml folder`.

| Parameter Name      | Required | Allowed Values                       | Description |
| ------------------- | -------- | ------------------------------------ | ----------- |
| createWorkspace     | x        | bool: true, false                    | Create Workspace if it could not be loaded |
| name                | x        | str                                  | For more details please read [here](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py#create-name--auth-none--subscription-id-none--resource-group-none--location-none--create-resource-group-true--sku--basic---friendly-name-none--storage-account-none--key-vault-none--app-insights-none--container-registry-none--cmk-keyvault-none--resource-cmk-uri-none--hbi-workspace-false--default-cpu-compute-target-none--default-gpu-compute-target-none--exist-ok-false--show-output-true-) |
| friendlyName        |          | str                                  |
| createResourceGroup |          | bool: true, false                    |
| location            |          | str: [supported region](https://azure.microsoft.com/global-infrastructure/services/?products=machine-learning-service) |
| sku                 |          | str: "basic", "enterprise"           |
| storageAccount      |          | str: Azure resource ID format        |
| keyVault            |          | str: Azure resource ID format        |
| appInsights         |          | str: Azure resource ID format        |
| containerRegistry   |          | str: Azure resource ID format        |
| cmkKeyVault         |          | str: Azure resource ID format        |
| resourceCmkUri      |          | str: URI of the customer managed key |
| hbiWorkspace        |          | bool: true, false                    |


### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples



### Using the optional input

This is how to use the optional input.

```yaml
with:
  myInput: world
  anotherInput: optional
```

### Using outputs

Show people how to use your outputs in another action.

```yaml
steps:
- uses: actions/checkout@master
- name: Run action
  id: myaction

  # Put your action name here
  uses: me/myaction@master

  # Put an example of your mandatory arguments here
  with:
    myInput: world

# Put an example of using your outputs here
- name: Check outputs
    run: |
    echo "Outputs - ${{ steps.myaction.outputs.myOutput }}"
```
