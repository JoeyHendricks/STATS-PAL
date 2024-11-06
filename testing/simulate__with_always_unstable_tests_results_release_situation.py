from testing.simulators import SimulateScenario

# will create the fictitious scenario object
scenario = SimulateScenario(
    baseline_id="RID-3",
    benchmark_id="RID-4",
    data_set_location="C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest"
                      "\\data\\hendricks\\raw-performance-test-data-001.csv"
)

# will run the scenario
scenario.run_original_scenario(
    order_of_comparison=[

        {"instructions": ["RID-1", "RID-2"]},
        {"instructions": ["RID-2", "RID-3"]},
        {"instructions": ["RID-3", "RID-4"]},
        {"instructions": ["RID-4", "RID-5"]},
        {"instructions": ["RID-5", "RID-6"]}
    ]
)
