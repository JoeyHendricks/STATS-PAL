from utilities.data import ConvertCsvResultsIntoJson

ACC = "C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest\\data\\real-world-raw-performance-test-data.csv"
prod = "C:\\Users\\joeyh\\PycharmProjects\\PercentileHypothesisTest\\data\\raw_data_prod_anoniem.csv"

response_times_prod = ConvertCsvResultsIntoJson(
    prod
).data
response_times_acc = ConvertCsvResultsIntoJson(
    ACC
).data
