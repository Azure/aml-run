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
    markdown = ""
    for k in metrics_dict.keys():
        markdown += f"## {k} \n\n"

        # format headers
        headers = "|"
        for nam in metrics_dict[k].keys():
            headers += f" {nam} |"
        markdown += headers + "\n"

        # add lines under headers
        markdown += "|" + " -- |" * len(metrics_dict[k]) + "\n"

        # add values
        metrics = "|"
        for val in metrics_dict[k].values():
            try:
                val = float(val)
                metrics += f" {val:.3} |"
            except ValueError:
                metrics += f" {val} |"
        markdown += metrics + "\n"

    return markdown
