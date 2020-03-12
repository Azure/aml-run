import os
import json

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.exceptions import AuthenticationException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError


def main():
    # Loading input values
    print("::debug::Loading input values")
    parameters_file = os.environ.get("INPUT_PARAMETERSFILE", default="run.json")
    azure_credentials = os.environ.get("INPUT_AZURECREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
    except ValueError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        return

    # Loading parameters file
    print("::debug::Loading parameters file")
    parameters_file_path = os.path.join(".aml", parameters_file)
    try:
        with open(parameters_file_path) as f:
            parameters = json.load(f)
    except FileNotFoundError:
        print(f"::error::Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository (e.g. .aml/workspace.json).")
        return

    # Loading Workspace
    print("::debug::Loading AML Workspace")
    sp_auth = ServicePrincipalAuthentication(
        tenant_id=azure_credentials.get("tenantId", ""),
        service_principal_id=azure_credentials.get("clientId", ""),
        service_principal_password=azure_credentials.get("clientSecret", "")
    )
    config_file_path = os.environ.get("GITHUB_WORKSPACE", default=".aml")
    config_file_name = "aml_arm_config.json"
    try:
        ws = Workspace.from_config(
           path=config_file_path,
           _file_name=config_file_name,
           auth=sp_auth
       )
    except AuthenticationException as exception:
        print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        return
    except AuthenticationError as exception:
        print(f"::error::Microsoft REST Authentication Error: {exception}")
        return
    except AdalError as exception:
        print(f"::error::Active Directory Authentication Library Error: {exception}")
        return

    # TODO: Create and submit run.
    print(parameters)
    print(ws)
    print("::debug::Successfully finised Azure Machine Learning Train Action")


if __name__ == "__main__":
    main()
