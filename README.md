<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/read-me-banner.png?raw=true"/>
</p>

<!-- INTRO -->
## In a nutshell what is this project all about?

Continuous performance testing is nothing new, but one of the biggest pitfalls of a reliable automated performance test 
is the manual analysis of its results. This manual intervention slows down the pace required to keep up with our ever 
more demanding online world. 

By verifying automatically if there's a significant change in behavior and producing a metric to represent the change 
between your baseline and benchmark we can speed up our testing effort, reduce our time to market and liberate a 
performance engineer to focus on more pressing matters.

This project hopes to bring a helping hand to performance engineers around the globe by providing them with a 
solution that can be embedded in their testing process to reliably perform complicated 
comparison analysis in an automated fashion. 

## Quickly get started comparing the results of two performance tests.

How you can get started using the code written in this project is easy first download the source code specifically the
[StatisticalDistanceTest](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/heuristic_test_result_comparisons/kolmogorov_smirnov_and_wasserstein.py) 
class from this repository after you have done that. You can give this class two arrays of raw response time 
measurements and compute the relevant statistics this can be done in the following manner:

```python
from heuristic_test_result_comparisons.kolmogorov_smirnov_and_wasserstein import StatisticalDistanceTest
from data import file_location_hendricks_raw_data_set_001  # <-- My primary example data set.
from data.wranglers import ConvertCsvResultsIntoDictionary

# As an example I provided a way to quickly convert a csv file into a Python dictionary.
raw_data = ConvertCsvResultsIntoDictionary(file_location_hendricks_raw_data_set_001).data

# Run the distance test against the given data.
stats_distance_test = StatisticalDistanceTest(
    population_a=raw_data["RID-1"]["response_times"],
    population_b=raw_data["RID-2"]["response_times"]
)

# Below printed information can be used to control a CI/CD pipeline. 
print(stats_distance_test.kolmogorov_smirnov_distance)  # >> 0.096
print(stats_distance_test.wasserstein_distance)         # >> 0.100
print(stats_distance_test.score)                        # >> 89.70
print(stats_distance_test.rank)                         # >> C

```
That is it you are all set now to embed advanced statistical analyse into your CID/CD pipeline, so you can make better
automated decisions when to continue the pipeline or halt it and raise a defect. As this comparison is not without 
its pitfalls and complexity ***I would recommend continuing to read below*** on how this comparison works and how you can 
best interpret its powerful information.

## Start using the raw format of your performance test results.

The calculations behind this project rely heavily on having every single measurement from your performance 
test available. This is commonly known as [raw data](https://en.wikipedia.org/wiki/Raw_data) in statistics. 

> It could be that you are unfamiliar with this term within the performance testing context and its philosophy within our industry. 
> I would recommend you to read through some of my mentor [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) excellent Linkedin 
> [articles](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) that cover this topic in great detail.

Why this raw format of your test results is so powerful can be best seen in the graph animation below. 

<!-- Raw Data Vs Averages animation -->
<img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>

The first view that is shown in the animation is the average response time over a time axis. 
In this view, we can see that the response time patterns of the system are relatively stable, 
but once the overlay switches to the raw data scatter plot (Keep in mind that both views are the same test.).
We can see a completely different picture of a system that is not quite as stable as the average 
line graph would have us believe.

As can be seen in this example is that the aggregation of data hides the actual performance of 
our system under test and gives us a false understanding of what the real patterns are.

Because of this reason, this project is based on this raw data philosophy from [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) 
that is why we base our automated analysis, not on a single simple metric like the average or the median, but we look 
into discovering change throughout the entire raw data set using more advanced statistical methods to 
verify how much the change between to tests is. 

***That is why using raw data is a prerequisite for being able to use the [heuristic](https://en.wikipedia.org/wiki/Heuristic) 
that is developed without raw data, it makes less sense to use this solution as aggregation could have "poisoned" our 
data and make it harder to give an accurate assessment.***.

## Statistical Distance

When automating performance testing and its analysis into a CI/CD pipeline we only would like to be notified if 
our results contain an interesting change in performance or behavior. In other words, we would only like to view our 
results when the [distance](https://en.wikipedia.org/wiki/Statistical_distance) between our baseline, and our benchmark 
increases or decreases. 

When this happens we can create a defect and start doing some research on why it is different
and to do this we would need to find out how much "distance" there is between our tests.
When talking about measuring the distance between our benchmark and baseline tests I am talking about finding the
[statistical distance](https://en.wikipedia.org/wiki/Statistical_distance) between two [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)) 
[cumulative distribution function (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function) which we have 
calculated from our raw data.

## Kolmogorov-Smirnov Distance

The Kolmogorov-Smirnov Distance is a distance metric that is calculated when using the very well known  
[Two Sample Kolmogorov-Smirnov Hypothesis Test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
This distance is very interesting as it represents the largest absolute difference between two 
[cumulative distribution function (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function).
Why this is interesting is clear when know the exact amount of maximum distance between two performance test
we could quantify how much is distance is too much and pass or fail a build based on that metric, we can call this
number a metric as it meets the formal four conditions to be considered a 
[metric](https://en.wikipedia.org/wiki/Statistical_distance).

In the case below we can verify that between the baseline and benchmark test largest distance between our 
two distributions is **0.207**:

<!-- KS distance example -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov-smirnov-absolute-distance-example.png"/>
</p>
The equation for the Kolmogorov-Smirnov distance is as follows:


<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov_smirnov_distance_equation.png"/>
</p>

When using Python you can calculate the Kolmogorov-Smirnov Distance in the following way using the 
[scipy](https://www.scipy.org/) package.

```python
from scipy.stats import ks_2samp

# An example array
baseline_cumulative_distribution_function = [1, 2, 3, 4]
benchmark_cumulative_distribution_function = [1, 2, 3, 4]

# Running a two sample Kolmogorov-Smirnov test and extracting the KS distance from it.
kolmogorov_smirnov_distance, kolmogorov_smirnov_probability = ks_2samp(
    baseline_cumulative_distribution_function,
    benchmark_cumulative_distribution_function
)
```
> More information on the Kolmogorov-Smirnov Distance can be found 
> [here](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) on Wikipedia

## Wasserstein Distance

The [Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric), also known as the 
[Earth Mover’s distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance) is formally quite difficult to 
understand it but by using its physical interpretation it is very easy to wrap your head around it. 

Consider your baseline as a pile of dirt, and your benchmark as a pile of dirt the goal is to match the height of 
the pile of dirt from the baseline to the benchmark. The energy or in other words the minimum amount of dirt or work 
required to create two equally sized piles of dirt is this is the Wasserstein distance.

## Computing the Wasserstein & Kolmogorov-Smirnov Distance from raw data

We would like to see how these two distance metrics react when keep changing the benchmark distribution from 
the baseline distribution before we can do this we would need to understand how we can calculate these two numbers 
from a normalized CDF. 

Luckily the [scipy](https://www.scipy.org/) package for Python has us covered you can calculate the 
first distance metric the [Kolmogorov-Smirnov Distance](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) 
the following way in Python:

```python
from scipy.stats import ks_2samp

# An example array
baseline_cumulative_distribution_function = [1, 2, 3, 4]
benchmark_cumulative_distribution_function = [1, 2, 3, 4]

# Running a two sample Kolmogorov-Smirnov test and extracting the KS distance from it.
kolmogorov_smirnov_distance, kolmogorov_smirnov_probability = ks_2samp(
    baseline_cumulative_distribution_function,
    benchmark_cumulative_distribution_function
)

```

The [Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric) can also be calculated similarly:

```python
from scipy.stats import wasserstein_distance

# An example array
baseline_cumulative_distribution_function = [1, 2, 3, 4]
benchmark_cumulative_distribution_function = [1, 2, 3, 4]

# Finding the Wasserstein distance
wasserstein = wasserstein_distance(
    baseline_cumulative_distribution_function,
    benchmark_cumulative_distribution_function
)

```

To find out how these metrics react to a continuously deteriorating benchmark I have performed the following experiment 
to see how these metrics react when distance is randomly introduced into two similar test.

<!-- ECDF Curve Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/wasserstein_and_kolmogorov_smirnov_simulation.gif?raw=true"/>
</p>

> Above you can see the results in the top right corner above the legend you can see the ***amount of distance introduced 
> in percentage*** this amount change is then spread out over 100% of the data set. At the bottom of this animation you 
> can view the increasing Wasserstein and Kolmogorov-Smirnov Distance metrics.

If you want to execute the above experiment for yourself you can do that by executing the following code in this
project:

```python
from simulations.simulators import SimulateFictitiousScenario

# Will create the fictitious scenario object from my default example data
scenario = SimulateFictitiousScenario(
    baseline_id="RID-3",
    benchmark_id="RID-4",
    data_set_location="your/path/here/raw-performance-test-data-001.csv"
)

# will run the scenario and randomly increase 100% of the data by 0% to 99%. 
# (increasing in percentage every simulation)
scenario.run_consistently_increase_benchmark_scenario(
    percent_of_data=100,
    save_image=False,
    show_image=False,  # <-- Watch out will spam your browser full
    repeats=0  # <-- amount of repeats per increase (increases are randomly distributed.)
)

```

## Ranking and scoring performance test results


For this project, I have chosen one of my own raw data test sets to verify if the heuristic which is 
created in the project is working as expected. This data in its raw format looks the following way in a 
simple scatter plot:

<!-- Example raw data scatter plot -->
<img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-001.png?raw=true"/>

> To briefly explain this graph each differently coloured point in the scatter plot is a different action 
> in my test. On the X axis the epoch timestamps are plotted from left to right and on the Y axis I have plotted 
> the response time in seconds on a logarithmic scale, for reference I have also plotted an average line for each panel.

## Resources I found while learning about this topic

- [An article from data dog about selecting statistical distance for machine learning.](https://www.datadoghq.com/blog/engineering/robust-statistical-distances-for-machine-learning/)

___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/issues">- Report Bug or Request Feature</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>

