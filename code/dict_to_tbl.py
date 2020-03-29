my_dict = {'GitHubActionExperiment_1585252332_b5f3cd66': {'Kernel type': 'linear', 'Penalty': 1.0, 'Accuracy': 0.9333333333333333, 'precision': 0.9333333333333333, 'recall': 0.9333333333333333, 'f1-score': 0.9333333333333333, 'confusion_matrix': 'aml://artifactId/ExperimentRun/dcid.GitHubActionExperiment_1585252332_b5f3cd66/confusion_matrix', 'confusion_matrix_unnormalized': 'aml://artifactId/ExperimentRun/dcid.GitHubActionExperiment_1585252332_b5f3cd66/confusion_matrix_unnormalized_1585253019.png', 'confusion_matrix_normalized': 'aml://artifactId/ExperimentRun/dcid.GitHubActionExperiment_1585252332_b5f3cd66/confusion_matrix_normalized_1585253019.png', 'Model Name': 'model.pkl'}}
markdown = ""
for k in my_dict.keys():
    markdown += f"## {k} \n\n"

    # format headers
    headers = "|"
    for nam in my_dict[k].keys():
        headers += f" {nam} |"
    markdown += headers + "\n"

    # add lines under headers
    markdown += "|" + " -- |"*len(my_dict[k]) + "\n"

    # add values
    metrics = "|"
    for val in my_dict[k].values():
        try:
            val = float(val)
            metrics += f" {val:.3} |"
        except ValueError:
            metrics += f" {val} |"
    markdown += metrics + "\n"

print(markdown)
