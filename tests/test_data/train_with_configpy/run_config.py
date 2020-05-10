from azureml.core import ComputeTarget
from azureml.train.estimator import Estimator


def main(workspace):
    # Loading compute target
    print("Loading compute target")
    compute_target = ComputeTarget(
        workspace=workspace,
        name="aml-intTest"
    )

    # Loading script parameters
    print("Loading script parameters")
    script_params = {
        "--kernel": "linear",
        "--penalty": 0.9
    }

    # Creating experiment config
    print("Creating experiment config")
    estimator = Estimator(
        source_directory="./tests/test_data/train_with_configpy",
        entry_script="train.py",
        script_params=script_params,
        compute_target=compute_target,
        conda_dependencies_file="environment.yml"
    )
    return estimator