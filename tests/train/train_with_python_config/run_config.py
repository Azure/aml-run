from azureml.core import ComputeTarget
from azureml.core import ScriptRunConfig, Environment


def main(workspace):
    # Loading compute target
    print("Loading compute target")
    compute_target = ComputeTarget(
        workspace=workspace,
        name="aml-intTest"
    )

    # Loading Environment
    print("Loading Environment")
    environment = Environment.from_conda_specification(
        name="myenv",
        file_path="tests/train/train_with_python_config/environment.yml"
    )

    # Loading script parameters
    print("Loading script parameters")
    script_args = [
        "--kernel", "linear",
        "--penalty", 1.0
    ]

    # Creating run config
    print("Creating run config")
    run_config = ScriptRunConfig(
        source_directory="tests/train/train_with_python_config",
        script="train.py",
        arguments=script_args,
        run_config="",
        compute_target=compute_target,
        environment=environment
    )
    return run_config
