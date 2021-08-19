from scipy.stats import ks_2samp, ttest_ind, f_oneway, chisquare
from data import response_times_acc90
from scipy import stats
import numpy as np
from utilities.helpers import calculate_percentile, normalize_distribution

PERCENTILE_DISTRIBUTION = [

    5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15,
    16, 17, 18, 19, 20,
    21, 22, 23, 24, 25,
    26, 27, 28, 29, 30,
    31, 32, 33, 34, 35,
    36, 37, 38, 39, 40,
    41, 42, 43, 44, 45,
    46, 47, 48, 49, 50,
    51, 52, 53, 54, 55,
    56, 57, 58, 59, 60,
    61, 62, 63, 64, 65,
    66, 67, 68, 69, 70,
    71, 72, 73, 74, 75,
    76, 77, 78, 79, 80,
    81, 82, 83, 84, 85,
    86, 87, 88, 89, 90,
    91, 92, 93, 94, 95,

]


def students_t_test(group_a, group_b):
    """

    :param group_a:
    :param group_b:
    :return:
    """
    t_value, p_value = ttest_ind(group_a, group_b)
    critical_t_value = stats.t.ppf(q=1-0.05 / 2, df=len(group_a) - 2)
    if p_value > 0.05:
        print("FAILED there is change")

    else:
        print("PASSED no change")

    print(f" the t value {t_value}")
    print(f" the critical t value {critical_t_value}")
    print(f" the p value {p_value}")
    print(f" the critical p value 0.05")
    print("----")


def kolmogorov_smirnov_test(group_a, group_b):
    """

    :param group_a:
    :param group_b:
    :return:
    """

    sample_size_a = len(group_a)
    sample_size_b = len(group_b)
    d_value, p_value = ks_2samp(group_a, group_b)
    critical_d_value = 1.36 * np.sqrt((sample_size_a + sample_size_b) / (sample_size_a * sample_size_b)) #stats.ksone.ppf(1-0.05/2, 30)

    if p_value > 0.05:
        print("NO CHANGE")

    else:
        print("CHANGE")

    print(f" the d value {d_value}")
    print(f" the critical d value {critical_d_value}")
    print(f" the p value {p_value}")
    print(f" the critical p value 0.05")
    print("----")


def anova_test(group_a, group_b):

    f_value, p_value = f_oneway(group_a, group_b)
    print(f" f-value: {f_value}")
    print(f" p-value: {p_value}")


normalize = False
bin_data_into_percentiles = False

sample_order = [
    {"data": ["RID-1", "RID-2"]},
    {"data": ["RID-2", "RID-3"]},
    {"data": ["RID-3", "RID-4"]},
    {"data": ["RID-4", "RID-5"]},
    {"data": ["RID-5", "RID-6"]},
    {"data": ["RID-1", "RID-6"]},

    {"data": ["RID-2", "RID-5"]},
    {"data": ["RID-3", "RID-5"]},
    {"data": ["RID-4", "RID-5"]},
]

for samples in sample_order:
    print(samples["data"])
    a = response_times_acc90[samples["data"][0]]["response_times"]
    b = response_times_acc90[samples["data"][1]]["response_times"]
    if normalize is True:
        a = normalize_distribution(a)
        b = normalize_distribution(b)
    if bin_data_into_percentiles:
        a = [calculate_percentile(a, percentile) for percentile in PERCENTILE_DISTRIBUTION]
        b = [calculate_percentile(b, percentile) for percentile in PERCENTILE_DISTRIBUTION]

    kolmogorov_smirnov_test(
        group_a=a,
        group_b=b
    )


