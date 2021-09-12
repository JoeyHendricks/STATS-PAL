from simulations.simulators import SimulateFictitiousScenario

# will create the fictitious scenario object
scenario = SimulateFictitiousScenario(
    baseline_id="RID-3",
    benchmark_id="RID-4",
    data_set_location="C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest"
                      "\\data\\hendricks\\raw-performance-test-data-001.csv"
)

# will run the scenario
scenario.run_consistently_increase_benchmark_scenario(
    percent_of_data=100,
    save_image=False,
    show_image=False,
    repeats=0
)
