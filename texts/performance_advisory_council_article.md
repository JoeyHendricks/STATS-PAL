<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/banner.png?raw=true"/>
</p>

___

**Our beautiful digital world is changing faster every day and with increased speed comes unprecedented more demand for 
automating more complex actions so organizations can pick up speed and face our ever more demanding online world.**

**Because of this demand, there is nothing new for performance engineering experts to execute their tests continuously. 
However, when integrating their entire quality assurance process into a pipeline we quickly recognize that the analysis 
of our complex test results is not an easy hurdle to overcome.**

## Please don’t bother me unless it is important

But what does it mean to analyze our test results automatically in a pipeline? In my opinion, it means that one 
wants to be able to trust an automatic analysis completely and only be prompted to look at test results when there 
is an interesting difference. Otherwise, we would want to let it go to production without any manual intervention as our 
automated analysis has determined that there is no significant risk. 

## Keep your data raw

When learning the ropes to become a performance engineer my mentor and good friend 
[Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) would always hammer in the importance of using raw data 
and, you know what the man is absolutely right.

Because of him, I realized that Raw data is a powerful tool that we have at our disposal to truly study how the 
system we are testing is acting, looking at the example below this becomes very evident when we look at an average 
line graph versus a raw scatter plot.

<!-- Raw Data Vs Averages animation -->
<p style="float: left;">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>
</p>

> If you want to learn more about raw data I would recommend reading Stijn's 
> [work](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) 
> on the matter as he has covered this topic very extensively.

**Keep in mind that both illustrations are from the same test** and that these results make it painstakingly clear 
that averages hide the actual behavior while the raw data show exactly what behavior or application has been portraying. 

Because of the magnificent detail, raw data presents us we would any automated decision-making to be based solely 
on the raw version of test results and not an aggregated or averaged out data set as this will make our calculation 
simply inaccurate. 

## 1.5 meters distance, please!

During this pandemic, you for sure have seen signs everywhere reminding you to keep your 
[distance](https://en.wikipedia.org/wiki/Statistical_distance)  from your fellow man. But what does 
[distance](https://en.wikipedia.org/wiki/Statistical_distance)  mean when we are analyzing our performance test 
results? In a sense, it implies that we would like to know how much difference there is between a baseline and a 
completed benchmark test.

In the field of statistics, there are a lot of distance metrics that can quantify to us how much distance there is 
between two tests one of these metrics which is utterly great for our use case is the 
[Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric) the equation to calculate this metric goes 
as follows:

<!-- Wasserstein distance equation -->
<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/wasserstein_distance_equation.png"/>
</p>

For most people, this formula would like some ancient runic spell which makes it a bit daunting to start learning 
more about this metric. However, understanding this metric becomes a lot easier when we look at its physical example:

*Consider this, both your baseline and benchmark test results are piles of dirt. Your boss asks you to make the 
benchmark pile of dirt as large as the baseline pile. The amount of work or in other words the amount of dirt required 
to make both piles the same size is the Wasserstein Distance which is why it is also known as the 
[Earth Mover’s distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance).*

Another metric that is great to determine how much distance there is between two performance tests would be the 
Kolmogorov-Smirnov Distance which is calculated when doing the very well-known 
[Kolmogorov-Smirnov hypothesis test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).

Kolmogorov-Smirnov distance metric is great because it indicates to us how much the absolute max amount of 
distance there is between our two tests, the equation for this is also quite complicated and looks like this:

<!-- KS distance equation -->
<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov_smirnov_distance_equation.png"/>
</p>

Truly understanding how this metric and the previous one are calculated is not needed to interpret these 
statistics. What is needed is knowing what they represent that way you can create a 
[heuristic](https://en.wikipedia.org/wiki/Heuristic) around these metrics to automatically assess if the 
difference between two performance tests is relatively normal.

## Letter ranks 

Understanding that the Wasserstein & Kolmogorov-Smirnov Distance exists is cool and all but how can we use these two 
metrics to rank our performance test results? Well for this I love using letter ranks as they are well known around 
the world and easy to understand by non-technical people.

To be able to rank our metrics, I have determined what our critical values are for both the Wasserstein and 
Kolmogorov-Smirnov Distances. With these critical values, we can categorize our test results into ranks ranging 
from S to F. Similar to what you would use to see back in older Japanese video games. 

In this table I have outlined what each letter rank would mean and which critical values and actions are associated 
with it:

| Impact Category  | Rank | Kolmogorov-Smirnov Distance boundary | Wasserstein Distance boundary | Possible Action |
|-----------|------|--------------------------------------|-------------------------------|-----------------|
| Negligible difference | S | 0.080 | 0.030 | No action required |
| Very Low | A | 0.150 | 0.060 | No action required |
| Low | B | 0.180 | 0.100 | Go for release create minor defect (or halt) |
| Medium | C | 0.220 | 0.125 | Halt release and create defect |
| High | D | 0.260 | 0.150 | Halt release and create defect |
| Very High | E | 0.300 | 0.200 | Halt release and create defect |
| Ultra | F | 0.340 | 0.250 | Halt release and create defect |

When creating a heuristic out of the data that is outlined in the table above we can start ranking our performance test 
results. To give you a visual example of how much distance is tolerated by each rank I have created the following 
animation where I consistently increase the amount of distance between our baseline and benchmark.

<!-- Ranking Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/ranking_simulation.gif?raw=true"/>
</p>

> Both benchmark and baseline test results are transformed into a [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)) 
[cumulative distribution function (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function), 
> so we can have an idea of what the probability is that a particular response time is produced by the application 
> we are testing.

Now that we understand these distance metrics and know that they can help us find out how different our performance 
test results are from each other we can start automating this analysis in Python.
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
liberate a performance engineer from a complex manual task. 

Freeing an engineer up to tackle more pressing matters and allowing DevOps teams to take up more slack when 
it comes to interpreting the results of performance tests that have been executed for them.
If you want to learn more about this topic I would suggest that you take a look at my GitHub repository. 

___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis">- Visit the project</a> -
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/texts/contributing_data.md"> Share your raw data</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>

