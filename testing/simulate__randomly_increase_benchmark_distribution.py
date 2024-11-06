from testing.simulators import SimulateScenario

# will create the fictitious scenario object
scenario = SimulateScenario(
    baseline_id="RID-4",
    benchmark_id="RID-4",
    data_set_location="C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest"
                      "\\data\\hendricks\\raw-performance-test-data-001.csv"
)

# will run the scenario
scenario.run_consistently_changing_benchmark_fictitious_scenario(
    percent_of_data=100,
    save_image=True,
    show_image=False,
    image_type="scatter",
    repeats=0,
    positive=True  # consistently increase
)
