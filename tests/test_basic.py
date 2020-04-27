#!/usr/bin/env python3
import os
import pytest
import sys
import json
from azureml.exceptions import AuthenticationException, ProjectSystemException, AzureMLException, UserErrorException

@pytest.fixture(autouse=True)
def set_env_variables():
    sys.path.append(os.path.join(os.path.dirname(__file__), '../code/'))
    os.environ["GITHUB_REPOSITORY"] ="https://github.com/test/"
    os.environ["GITHUB_REF"] ="test_basic"
    os.environ["INPUT_PARAMETERS_FILE"] ="ashkuma"
    os.environ["INPUT_AZURE_CREDENTIALS"] = ' { "clientId": "123", "clientSecret": "123", "subscriptionId": "123", "tenantId": "123"}'
    os.environ["GITHUB_WORKSPACE"] ="./"
    
    yield
    # a test may override the base info so after yield it resets
    os.environ["GITHUB_REPOSITORY"] ="https://github.com/test/"
    os.environ["GITHUB_REF"] ="test_basic"
    os.environ["INPUT_PARAMETERS_FILE"] ="ashkuma"
    os.environ["INPUT_AZURE_CREDENTIALS"] = ' { "clientId": "123", "clientSecret": "123", "subscriptionId": "123", "tenantId": "123"}'
    os.environ["GITHUB_WORKSPACE"] ="./"
    

def test_credentialErrorException():
    """unit Test to verify that in azure credentials are not present code must raise the error """
    os.environ["INPUT_AZURE_CREDENTIALS"] = ''
    import main
    import actionutils
    with pytest.raises(actionutils.AMLConfigurationException):
        assert main.main()

def test_parametersfileError():
    """unit Test to verify that if  aml_arm_config.json file is not present the raise this error """
    os.environ["INPUT_PARAMETERS_FILE"] = 'wrongfile.json'
    import main
    with pytest.raises(UserErrorException):
        assert main.main()


if __name__ == "__main__":
    pass