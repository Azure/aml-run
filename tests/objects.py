markdown_conversion_input = {
        "5815b172-61fe-4e8d-baa2-e4ffe33e77d3": {
            "testkey": "testvalue"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233": {
            "best_child_by_primary_metric": {
                "metric_name": ["mse", "mse"],
                "timestamp": ["2020-04-06 16:04:23.719570+00:00", "2020-04-06 16:04:23.719570+00:00"],
                "run_id": ["HD_7034e363-3172-41e6-8423-eb292f39e233_1", "HD_7034e363-3172-41e6-8423-eb292f39e233_1"],
                "metric_value": [0.025010755222666936, 0.025010755222666936],
                "final": [False, True]
            }
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_0": {
            "auc": 0.6394267984578837,
            "mse": 0.025010755222666936,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_1": {
            "auc": 0.6394267984578837,
            "mse": 0.025010755222666936,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png"
        },
        "HD_7034e363-3172-41e6-8423-eb292f39e233_2": {
            "mse": 0.025010755222666936,
            "auc": 0.6394267984578837,
            "TimeSeries comparison": "aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png"
        }
    }

markdown_out = """## Run Details:%0A%0A Experiment/Pipeline ID: 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 %0A%0A| Run ID | Parameter | Value |%0A| ----- | ----- | ----- |%0A| 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 | testkey | testvalue |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png |%0A"""