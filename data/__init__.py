from utilities.generator import ConvertCsvResultsIntoJson


real_world_raw_performance_test_data = ConvertCsvResultsIntoJson(
    "C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest\\data\\real-world-raw-performance-test-data.csv"
).data
