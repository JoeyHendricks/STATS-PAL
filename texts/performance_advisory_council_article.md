<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/banner.jpg?raw=true"/>
</p>

___

**Our beautiful digital world is changing faster every day and with increased speed comes an unprecedented increase in 
demand for automating complex actions so organizations can save time and pick up speed and be ready to face the ever 
more demanding online world.**

**Because of this demand for automation, there is nothing new to continuously execute performance tests in an CI/CD 
pipeline. However, when integrating our performance testing process into a pipeline, we quickly recognize that 
automating the analysis of our complex test results is not an easy to hurdle to overcome.**

## Please don’t bother me unless it is important

So, what does it mean to analyze our test results automatically in a pipeline? In my opinion, it means that one wants 
to be able to trust an automatic analysis completely and only be prompted to look at test results when there is an 
interesting difference. Otherwise, we would want to let it go to production without any manual intervention as our 
automated analysis has determined that there is no significant risk.

I have realized that raw data is a powerful tool that we have at our disposal to truly study how the system we are 
testing is acting. This becomes quite evident when we look at an average line graph versus a raw scatter plot as 
given below.

<!-- Raw Data Vs Averages animation -->
<p style="float: left;">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>
</p>

> If you want to learn more about raw data I would recommend reading 
> [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) 
> [work](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) 
> on the matter as he has covered this topic very extensively.

**Bear in mind that both illustrations** are from the same test and that these results make it painstakingly clear that 
averages hide the actual behavior while raw data shows exactly what kind of behaviour our application has been portraying.
Because of the magnificent detail, raw data perpetuates automated decision-making to be based solely on the raw 
version of test results and not an aggregated or averaged out data set as this will make our calculation simply 
inaccurate.

## 1.5 meters distance, please!

During this pandemic, you must have seen signs everywhere reminding you to keep 
[distance](https://en.wikipedia.org/wiki/Statistical_distance) from one another but what does
[distance](https://en.wikipedia.org/wiki/Statistical_distance) mean when we are analyzing our performance test 
results? In a sense, it implies that we would like to know how much difference there is between a baseline, 
and a completed benchmark test.

In the field of statistics, there are many [distance](https://en.wikipedia.org/wiki/Statistical_distance) metrics 
that can quantify the distance between two tests. One such metric which can be implemented  for our use case is 
the [Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric). The equation to calculate 
this metric is as follows:

<!-- Wasserstein distance equation -->
<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/wasserstein_distance_equation.png"/>
</p>

For most people, this equation would seem like some ancient runic spell which makes it a bit daunting to understand. 
However, understanding this equation becomes a lot easier when we look at its physical example:

*Consider this, both your baseline and benchmark test results are piles of dirt. Your boss asks you to make the 
benchmark pile of dirt as large as the baseline pile. The amount of work or in other words the amount of dirt required 
to make both piles the same size is the Wasserstein Distance which is why it is also known as the 
[Earth Mover’s distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance).*

Another metric that is useful for determining the distance between two performance tests is the 
Kolmogorov-Smirnov Distance which is calculated from the well-known 
[Two-Sample Kolmogorov-Smirnov Hypothesis Test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
Kolmogorov-Smirnov distance metric is a wonderful tool because it indicates the absolute maximum amount of 
distance between our two tests this is represented by this equation:

<!-- KS distance equation -->
<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov_smirnov_distance_equation.png"/>
</p>

It is not necessary to understand how these two metrics are calculated for interpreting their results. However, what 
is truly needed is knowing what they represent. This way, you can create a 
[heuristic](https://en.wikipedia.org/wiki/Heuristic) around these metrics to automatically assess if the difference 
between two performance tests is relatively normal.

## Letter ranks 

Understanding that the Wasserstein & Kolmogorov-Smirnov Distance exists is cool and all but how can we use these two 
metrics to rank our performance test results? Well, for this I love using letter ranks as they are well known around 
the world and are easy to understand by non-technical people.

To be able to rank our metrics, I have determined what are the critical values for both the Wasserstein and 
Kolmogorov-Smirnov Distances. With these critical values, we can categorize our test results into ranks ranging 
from S to F. This is similar to what was used in older Japanese video games.

| Impact Category  | Rank | Kolmogorov-Smirnov Distance boundary | Wasserstein Distance boundary | Possible Action |
|-----------|------|--------------------------------------|-------------------------------|-----------------|
| Negligible difference | S | 0.080 | 0.030 | No action required |
| Very Low | A | 0.150 | 0.060 | No action required |
| Low | B | 0.180 | 0.100 | Go for release create minor defect (or halt) |
| Medium | C | 0.220 | 0.125 | Halt release and create defect |
| High | D | 0.260 | 0.150 | Halt release and create defect |
| Very High | E | 0.300 | 0.200 | Halt release and create defect |
| Ultra | F | 0.340 | 0.250 | Halt release and create defect |

When creating a heuristic out of the data that is outlined in the table above, we can start ranking our performance 
test results. To give you a visual example of how much distance is tolerated by each rank, I have created the 
following animation where I consistently increase the amount of distance between our baseline and benchmark.

<!-- Ranking Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/ranking_simulation.gif?raw=true"/>
</p>

> Both benchmark and baseline test results are transformed into a 
> [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)) 
> [cumulative distribution function (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function), 
> so we can have an idea of what the probability is that a particular response time is produced by the application 
> we are testing.

Now that we understand these distance metrics and know that they can help us find out how different 
our performance test results are from each other, we can start automating this analysis in Python. 
For this purpose, I have written a class that can be 
[downloaded from my GitHub repository](https://github.com/JoeyHendricks/automated-performance-test-result-analysis).

Using this class is fairly simple as you only need to execute the following code like in the example below:

```python
from heuristics.kolmogorov_smirnov_and_wasserstein import StatisticalDistanceTest
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
print(stats_distance_test.wasserstein_distance)  # >> 0.100
print(stats_distance_test.score)  # >> 89.70
print(stats_distance_test.rank)  # >> C

```

> For more instructions and information please visit 
> [my GitHub repository](https://github.com/JoeyHendricks/automated-performance-test-result-analysis)

# Conclusion

Automating performance test result analysis is very well possible and can provide a lot of value as we can 
liberate performance engineers from complex manual labour. It lets engineers  tackle more pressing issues and 
allow DevOps teams to take up slack when it comes to interpreting the results of performance tests that have been 
executed for them. 

If this was an interesting read, and you want to learn more about this topic, I would suggest taking a look at my 
GitHub repository. 

___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis">- Visit the project</a> -
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/texts/contributing_data.md"> Share your raw data</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>

