class AMLConfigurationException(Exception):
    pass


class AMLExperimentConfigurationException(Exception):
    pass


def required_parameters_provided(parameters, keys, message="Required parameter not found in your parameters file. Please provide a value for the following key(s): "):
    missing_keys = []
    for key in keys:
        if key not in parameters:
            err_msg = f"{message} {key}"
            print(f"::error::{err_msg}")
            missing_keys.append(key)
    if len(missing_keys) > 0:
        raise AMLConfigurationException(f"{message} {missing_keys}")


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