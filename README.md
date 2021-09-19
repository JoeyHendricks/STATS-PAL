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

These CDF's sound difficult, but they really aren't they are quite easy to understand once you see how they and
information they are displaying. These graphs just show what the probability is that certain percentage is under
a certain value.

<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/empirical-cumulative-distribution-function-example.jpg"/>
</p>

> A very good explanation that helped me understand how to read CDF's can be best found John DeJesus article on this 
> topic you can find this article [here](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480).

## Computing the Kolmogorov-Smirnov Distance

The Kolmogorov-Smirnov Distance is a distance metric that is calculated when using the very well known  
[Two Sample Kolmogorov-Smirnov Hypothesis Test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
This distance is very interesting as it represents the largest absolute difference between two 
[cumulative distribution function (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function).

Why this is an interesting number because it tells us the exact amount of maximum distance between two performance test
with the max amount quantify we can go and define how much is distance is too much and pass or fail a build based on 
that one metric, keep in mind that we can call this number a metric as it meets the [formal four conditions to be 
considered a metric](https://en.wikipedia.org/wiki/Statistical_distance).

<!-- KS distance example -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov-smirnov-absolute-distance-example.png"/>
</p>

In this case we can verify that between the baseline and benchmark test largest distance between our 
two distributions is **0.207** as can be seen in the graph.

If you are interested in understanding the equation behind the Kolmogorov-Smirnov distance below you can find 
an image that shows the exact formula for more information I would recommend reading the excellent 
[Wikipedia article](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) on the subject.

<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov_smirnov_distance_equation.png"/>
</p>

To automate this equation we can use the amazing Python package [scipy](https://www.scipy.org/) to calculate 
in the Kolmogorov-Smirnov Distance in the following way using an example distribution:

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

## Computing the Wasserstein Distance

Another great metric is the [Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric), also known as the 
[Earth Mover’s distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance) it is formally quite difficult to 
understand as you can tell from just glancing at its Wikipedia article makes you believe it is written in elvish, but 
by using its physical interpretation it is very easy to wrap your head around it and understand what it does. 

Consider this, both your baseline and benchmark test results as a piles of dirt, your boss asks you to make the 
benchmark pile of dirt as large as the baseline pile. The amount of work or in other words the amount of dirt required 
to make both piles the same size is the Wasserstein Distance that is why it is also known as the Earth Mover’s distance.

For us performance engineers this metric is awesome as it quantifies how much difference there is between two tests.
Understanding that this metric stand for the work required to change one test into another we can also use this metric
to drive decisions making in a CI/CD pipeline.

The formal equation to calculate the Wasserstein Distance is as follows:

<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/wasserstein_distance_equation.png"/>
</p>

Similarly to Kolmogorov-Smirnov Distance we can automate this formula by 
using Python's [scipy](https://www.scipy.org/) package with the following code:

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

## Determining our critical values for distance metrics

We can very well understand that Wasserstein & Kolmogorov-Smirnov Distance are excellent metric that we can use
to define how much distance there is between two distributions, but I believe when both distance metrics would 
be included into a [heuristic](https://en.wikipedia.org/wiki/Heuristic) where we define boundaries that would outline
what we would consider how much distance we would tolerate.

To find out what these critical values are for us we would need to do an experiment where we take two stable 
performance tests and keep introducing more and more changes to them. That way we can quickly see what values 
we would consider being too much. 

Before it is possible to experiment we would need to select two very similar performance 
test results sets out of my primary example data set. 

<!-- Example raw data scatter plot -->
<p align="center">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-001.png?raw=true"/>
</p>

> To briefly explain this graph each differently coloured point in the scatter plot is a different action 
> in my test. On the X axis the epoch timestamps are plotted from left to right and on the Y axis I have plotted 
> the response time in seconds on a logarithmic scale, for reference I have also plotted an average line for each panel.

Above you can find the raw scatter plot of my favorite example data set you might have noticed that the 
two most stable tests out of this set are **RID-2 & RID-3**. That is why for this experiment we will take **RID-3 
as our baseline and RID-4 as our benchmark**. 

The code needed to execute this experiment is as follows:

```python
from simulations.simulators import SimulateScenario

# Will create the fictitious scenario object from my default example data
scenario = SimulateScenario(
    baseline_id="RID-3",
    benchmark_id="RID-4",
    data_set_location="your/path/here/raw-performance-test-data-001.csv"
)

# will run the scenario and randomly increase 100% of the data by 0% to 99%. 
# (increasing in percentage every simulation)
scenario.run_consistently_changing_benchmark_fictitious_scenario(
    percent_of_data=100,
    save_image=False,
    show_image=False,  # <-- Watch out will spam your browser full
    repeats=0  # <-- amount of repeats per increase (increases are randomly distributed.)
)
```

Out of the statistics, and the graphs that this code produces I have generated the following animation to
showcase how a continuously deteriorating benchmark faces up to a stable baseline:

<!-- ECDF Curve Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/wasserstein_and_kolmogorov_smirnov_simulation.gif?raw=true"/>
</p>

> Above you can see the results in the top right corner above the legend you can see the ***amount of distance introduced 
> in percentage*** this amount change is then spread out over 100% of the data set. At the bottom of this animation you 
> can view the increasing Wasserstein and Kolmogorov-Smirnov Distances.

## Ranking our distance metrics

From the information obtained from running our simple experiment we can determine for ourselves what we quantify as 
too much distance between two performance test. With this information we can then created a table of critical values 
that we can use to Rank our tests with a letter ranging from S to F (Japanese letter grading system like 
you used to see in old Sega video games.) based on these ranks we can start making automated decisions in a CI/CD pipeline.

| Impact Category  | Rank | Kolmogorov-Smirnov Distance boundary | Wasserstein Distance boundary | Possible Action |
|-----------|------|--------------------------------------|-------------------------------|-----------------|
| Negligible difference | S | 0.080 | 0.030 | No action required |
| Very Low | A | 0.150 | 0.060 | No action required |
| Low | B | 0.180 | 0.100 | Go to release create minor defect (or halt) |
| Medium | C | 0.220 | 0.125 | Halt and create defect |
| High | D | 0.260 | 0.150 | Halt and create defect |
| Very High | E | 0.300 | 0.200 | Halt and create defect |
| Ultra | F | 0.340 | 0.250 | Halt and create defect |

> When reading this table keep in mind that both statistics need fall in the same category if this is not the case
> the lowest category is selected.

For myself I have defined these critical values in the table above as they work nicely for my own data I am presuming
that is plausible that they will also work for most other applications as the amount of distance will always stay 
the same, but you could be tolerating more or less distance than me depending on your context. 

In practice this would mean that you could be accepting lower ranks as good, or you would only accept the highest rank
this all depends on your preference when you want to fail your build. When running the same experiment we used to 
determine our critical values but this time we are ranking our performance test results from S to F using our 
heuristic would yield the following results:

<!-- Ranking Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/ranking_simulation.gif?raw=true"/>
</p>

It is interesting to see that this ranking mechanism can filter out test that are different from the baseline but what 
happens when there is no interesting change between two runs? For that we would need a couple of very stable 
test results sets which we can compare for this reason I have created the following ten example tests that contain
a normal amount of difference to each other as you can tell from the image below:

<!-- Stable test runs -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-004.png?raw=true"/>
</p>

When these test are compared in the following order and pulled through our ranking 
mechanism we would get the following results:

| Baseline RunID | Benchmark RunID | Rank | Kolmogorov-Smirnov Distance | Wasserstein Distance |
|----------------|-----------------|------|-----------------------------|----------------------|
| RID-1 | RID-2 | S | 0.042 | 0.018 |
| RID-2 | RID-3 | S | 0.027 | 0.019 |
| RID-3 | RID-4 | S | 0.061 | 0.029 |
| RID-4 | RID-5 | S | 0.025 | 0.011 |
| RID-5 | RID-6 | S | 0.078 | 0.027 |
| RID-6 | RID-7 | S | 0.066 | 0.022 |
| RID-8 | RID-9 | S | 0.021 | 0.022 |
| RID-9 | RID-10 | A | 0.067 | 0.033 |

> You can run this experiment also for yourself by executing the following 
> [script from this project](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/simulations/simulate__with_always_stable_tests_results_no_regression.py).

In the previous example we tested test results that contain change but how our ranking mechanism would react to 
change can also be tested similarly for this we could use my favorite data set that contains a lot of different 
situations. You can interpret these results as different release moments where the release had a positive impact,
a negative impact and no impact below you can see the data set:

<!-- Example raw data scatter plot -->
<p align="center">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-001.png?raw=true"/>
</p>

When we also automatically analyze this data using our ranking mechanism we are left with the following results:

| Baseline RunID | Benchmark RunID | Rank | Kolmogorov-Smirnov Distance | Wasserstein Distance |
|----------------|-----------------|------|-----------------------------|----------------------|
| RID-1 | RID-2 | C | 0.142 | 0.120 |
| RID-2 | RID-3 | S | 0.062 | 0.025 |
| RID-3 | RID-4 | A | 0.091 | 0.040 |
| RID-4 | RID-5 | A | 0.057 | 0.055 |
| RID-5 | RID-6 | F | 0.283 | 0.255 |

> You can find the source code for this experiment also in the following 
> [file in the project](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/simulations/simulate__with_always_unstable_tests_results_release_situation.py).

When correlating the estimated rank to what we see in our scatter plot we can determine that each score justified as 
RID-2 to RID-5 are very similar in performance but have a low amount of difference one could accept as the amount of
distance is small it would therefore not directly impact our end users.

## Contribute to this project 

Help me to make result analysis easier for more performance engineers around the globe by donating your 
expertise and knowledge, anonymized test data or just by sharing this project on your socials together we 
can make this project smarter and more robust!

Feel free to open up an issue if you have any questions or are experiencing issues. 
**Want to contribute?** Then shoot in a pull request with your changes or test data, so we can continue 
to make improvements to this project. 

## Resources I found while learning about this topic

- [An article from data dog about selecting statistical distance for machine learning.](https://www.datadoghq.com/blog/engineering/robust-statistical-distances-for-machine-learning/)
- [How to read empirical cumulative distribution functions.](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480)
___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/issues">- Report Bug or Request Feature</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>

