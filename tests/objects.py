markdown_conversion_input_1 = {
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

markdown_conversion_output_1 = """## Run Details:%0A%0A Experiment/Pipeline ID: 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 %0A%0A| Run ID | Parameter | Value |%0A| ----- | ----- | ----- |%0A| 5815b172-61fe-4e8d-baa2-e4ffe33e77d3 | testkey | testvalue |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_0 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_0/TimeSeries comparison_1586189163.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_1 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_1/TimeSeries comparison_1586189032.png |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | mse | 0.025 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | auc | 0.639 |%0A| HD_7034e363-3172-41e6-8423-eb292f39e233_2 | TimeSeries comparison | aml://artifactId/ExperimentRun/dcid.HD_7034e363-3172-41e6-8423-eb292f39e233_2/TimeSeries comparison_1586189099.png |%0A"""

markdown_conversion_input_2 = {
    "Training samples": 353.0,
    "Test samples": 89.0,
    "alpha": 0.03,
    "mse": 3424.9003158960168
}

markdown_conversion_output_2 = """Output"""

markdown_conversion_input_3 = {
    "HD_9cbf07dc-db35-4700-adc3-92253a378992": {
        "best_child_by_primary_metric": {
            "metric_name": [
                "mse",
                "mse",
                "mse"
            ],
            "timestamp": [
                "2020-03-30 07: 58: 40.110108+00: 00",
                "2020-03-30 07: 59: 42.417631+00: 00",
                "2020-03-30 07: 59: 42.417631+00: 00"
            ],
            "run_id": [
                "HD_9cbf07dc-db35-4700-adc3-92253a378992_2",
                "HD_9cbf07dc-db35-4700-adc3-92253a378992_1",
                "HD_9cbf07dc-db35-4700-adc3-92253a378992_1"
            ],
            "metric_value": [
                0.4896792910300023,
                0.33284572706891424,
                0.33284572706891424
            ],
            "final": [
                False,
                False,
                True
            ]
        }
    },
    "HD_9cbf07dc-db35-4700-adc3-92253a378992_0": {
        "AUC": 0.6562945178135493,
        "RMSE": 0.05120842417634075,
        "pAUC": 0.2812047761829226,
        "mse": 0.9367719704449606,
        "TimeSeries comparison": "aml: //artifactId/ExperimentRun/dcid.HD_9cbf07dc-db35-4700-adc3-92253a378992_0/TimeSeries comparison_1585555145.png"
    },
    "HD_9cbf07dc-db35-4700-adc3-92253a378992_1": {
        "AUC": 0.3573103979675637,
        "pAUC": 0.5616569664904285,
        "RMSE": 0.6161010679565609,
        "mse": 0.33284572706891424,
        "TimeSeries comparison": "aml: //artifactId/ExperimentRun/dcid.HD_9cbf07dc-db35-4700-adc3-92253a378992_1/TimeSeries comparison_1585555146.png"
    },
    "HD_9cbf07dc-db35-4700-adc3-92253a378992_2": {
        "AUC": 0.1200601984180878,
        "pAUC": 0.5805687333099157,
        "RMSE": 0.09691275977364577,
        "mse": 0.4896792910300023,
        "TimeSeries comparison": "aml: //artifactId/ExperimentRun/dcid.HD_9cbf07dc-db35-4700-adc3-92253a378992_2/TimeSeries comparison_1585555076.png"
    }
}

markdown_conversion_output_2 = """Output"""
