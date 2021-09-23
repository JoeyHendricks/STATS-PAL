<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/banner.png?raw=true"/>
</p>

<!-- INTRO -->
## In a nutshell what is this project all about?

Continuous performance testing is nothing new, but one of the biggest pitfalls of a reliable automated performance test 
is the manual analysis of its results. This manual intervention slows down the pace required to keep up with our ever 
more demanding online world. 

By verifying automatically if there's a significant change in behavior and producing a rank or score to represent 
the difference between your baseline and benchmark we can speed up our testing effort, reduce our time to market and 
liberate a performance engineer to focus on more pressing matters.

This project hopes to bring a helping hand to performance engineers around the globe by providing them with a 
solution that can be embedded in their testing process to reliably perform complicated 
comparison analysis in an automated fashion. 

## Installation

Install this projects dependencies easily using [pip](https://pip.pypa.io/en/stable/) 
through the [requirements file](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/requirements.txt) 
you can use the following command to install them:

```bash
pip install -r /path/to/requirements.txt  
```

> If you are having trouble check out this [stack overflow article](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from/54405453#54405453).

## Quickly get started comparing the results of two performance tests.

How you can get started using the code written in this project is easy first, you download the source code specifically the 
[StatisticalDistanceTest](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/heuristic_test_result_comparisons/kolmogorov_smirnov_and_wasserstein.py) 
class from this repository. Secondly, you give this class two arrays of raw response time measurements and compute the 
relevant statistics this can be done in the following manner:

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
That is it! You are all set now to embed advanced statistical analysis into your very own CID/CD pipeline
This method will allow you to make a better-automated decision when to continue the pipeline or halt it and raise 
a defect. 

> This comparison is not without its pitfalls and complexity that is why ***I would strongly recommend you to continue 
> to reading and learn more*** about how this automated process works and how you can best interpret its powerful 
> results.

## Start using the raw format of your performance test results.

The calculations behind this project rely heavily on having every single measurement from your performance 
test available this is commonly known as [raw data](https://en.wikipedia.org/wiki/Raw_data).
This means that our data has not yet undergone any processing, which means that the data can not be an aggregated sample.

You might be unfamiliar with this term within the performance testing context and its philosophy within our industry. 
That is why I would recommend you to read through some of my mentor
[Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) excellent Linkedin 
[articles](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) 
that cover this topic in great detail.

To give you a visual example of why this raw format is great for finding weird and interesting patterns 
in your results you can best review the animation below:

<!-- Raw Data Vs Averages animation -->
<img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>

This animation shows us two views of the same performance test, the first view shows a line graph of the average 
response time. The second view shows the raw scatter plot where each measurement is shown.

It is clear from this example that there is a significant difference in both these views even though they are from 
the same test. It seems that the average line makes the performance of the application we are testing look better 
than it is while the scatter plot shows how the system is actually behaving.

If we would only have this average line graph at our disposal we could quickly have a false understanding of what the 
real response time patterns of our application are. Because of this reason, this project bases itself on the "raw data 
philosophy" from [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/). 

That is why base our automated decision-making process not on a single simple metric like the average or the median, 
but we look into discovering change throughout the data set, using more advanced statistical methods to verify how 
much the change between the two tests results is.

## Statistical Distance

When automating performance testing and its analysis into a CI/CD pipeline we only would like to be notified if 
our results contain an interesting shift in performance or behavior. 

In other words, we would only like to view our results when the [distance](https://en.wikipedia.org/wiki/Statistical_distance) 
between our baseline, and our benchmark has increased or decreased beyond a point that we could consider normal. 
When this happens, and an interesting difference has been introduced human intervention and follow-up analysis will 
be required therefore a defect can be created, and the pipeline halted.

To be able to halt a pipeline when two tests are significantly different from each other we would need to find a 
good way to measure how much "[distance](https://en.wikipedia.org/wiki/Statistical_distance)" there is between two 
tests. But what does [distance](https://en.wikipedia.org/wiki/Statistical_distance) mean? Well when 
talking about measuring the [distance](https://en.wikipedia.org/wiki/Statistical_distance) between our benchmark and 
baseline tests I am talking about finding the [statistical distance](https://en.wikipedia.org/wiki/Statistical_distance).

We could then convert our raw data into a [normalized](https://en.wikipedia.org/wiki/Normalization_(statistics)) 
[cumulative distribution functions (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function) and compare them 
using statistical methods. CDF's sound difficult, but they really aren't they are quite easy to 
understand once you see how they portray, the information they are displaying. In a nutshell, 
a CDF just shows what the probability is that a certain percentage is under a certain value.

<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/empirical-cumulative-distribution-function-example.jpg"/>
</p>

> A very good explanation that helped me understand how to read CDF's can be best found on John DeJesus excellent 
> article on this exact topic, you can find his article [here](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480).

## Computing the Kolmogorov-Smirnov Distance

The Kolmogorov-Smirnov Distance is a distance metric that is calculated when using the very well-known 
[Two-Sample Kolmogorov-Smirnov Hypothesis Test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test). 
This distance is fascinating as it represents the largest absolute difference between two 
[cumulative distribution functions (CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function).

Why this is an interesting metric for performance engineers is that it quantifies what the maximum amount of distance 
is between two tests. Knowing how significant this distance is can help us interpret if this metric lies within a 
certain degree of normalcy or if it has changed too much to be considered normal. The Kolmogorov-Smirnov distance
is an excellent metric that can help us figure out if our tests contain an unusual difference or not.

> Keep in mind that we can call this number a metric as it meets the [formal four conditions to be 
considered a metric](https://en.wikipedia.org/wiki/Statistical_distance).

<!-- KS distance example -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov-smirnov-absolute-distance-example.png"/>
</p>

In the case above, we have compared the two distributions (the red and blue line) against each other and calculated 
Kolmogorov-Smirnov distance which is **0.207**. As can be observed in the graph this number represents the absolute max 
distance between these two lines. The formula to calculate the Kolmogorov-Smirnov distance is as follows:

<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/kolmogorov_smirnov_distance_equation.png"/>
</p>

If you are interested in understanding the equation behind the Kolmogorov-Smirnov distance
I would recommend reading this great Wikipedia article [Wikipedia article](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
To automate this equation we can use the amazing Python package [scipy](https://www.scipy.org/) to calculate 
the Kolmogorov-Smirnov Distance in the following way using an example distribution:

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
understand this metric as you can tell from just glancing at its Wikipedia article which makes you believe it is written
in elvish. 

However, by using its physical interpretation it is easy to wrap your head around it and understand what it does:

*Consider this, both your baseline and benchmark test results are piles of dirt. Your boss asks you to make the 
benchmark pile of dirt as large as the baseline pile. The amount of work or in other words the amount of dirt 
required to make both piles the same size is the Wasserstein Distance which is why it is also known as the Earth 
Mover’s distance.*

Below you can see this concept in a graphical form the orange part between the red and blue line is the amount of
work required to change the red line into the blue one:

<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/wasserstein-overall-distance-example.png?raw=true"/>
</p>

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

Knowing that the Wasserstein & Kolmogorov-Smirnov Distance exists and understanding that these are excellent metrics 
that we can use to define how much distance there is between two distributions. Armed with this knowledge we can 
start thinking about creating a [heuristic](https://en.wikipedia.org/wiki/Heuristic) that can interpret these 
two complex numbers and come up with a score or rank, so we can categorize our results.

To do this we define boundaries for our heuristic that would outline how much distance we could tolerate between tests. 
To find these critical values we would need to do a simple experiment where we take two stable performance tests and 
keep introducing an increasing amount of change into them. That way we can immediately see what values we could consider 
as being too much.

Before it is possible to experiment we would need to select two very similar performance test results sets out of one 
of my example data set.

<!-- Example raw data scatter plot -->
<p align="center">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-001.png?raw=true"/>
</p>

> To briefly explain this graph each differently colored point in the scatter plot is a different action in my test. 
> On the X-axis the epoch timestamps are plotted from left to right and on the Y-axis I have plotted the response time 
> in seconds on a logarithmic scale, for reference I have also plotted an average line for each panel.

Above you can find the raw scatter plot of my favorite example data set you might have noticed that the 
two most stable tests out of this set are **RID-3 & RID-4**. That is why for this experiment we will take **RID-3 
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
    repeats=0,  # <-- amount of repeats per increase (increases are randomly distributed.)
    positive=True
)
```

Out of the statistics, and the graphs that this code produces I have generated the following animation to
showcase how a continuously deteriorating benchmark faces up to a stable baseline:

<!-- ECDF Curve Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/wasserstein_and_kolmogorov_smirnov_simulation.gif?raw=true"/>
</p>

> Above you can see the results in the top right corner above the legend in the title, you can see the amount of 
> distance introduced as a percentage this amount of change is then spread out over 100% of the data set. Furthermore, 
> at the bottom of this animation, you can view the increasing Wasserstein and Kolmogorov-Smirnov Distances for 
> reference.

## Ranking our distance metrics

From the information obtained from running our simple experiment, we can determine for ourselves what we quantify 
as too much distance between two performance tests. 

When we have this information we can then create a table of critical values. Within this table, we can then categorize 
our values into a Japanese letter rank ranging from S to F. (Just like you used to see in older video games).

Using these values in a heuristic we could estimate the letter rank and use that rank to pass or fail a pipeline.
In my case, these values are the following I believe that these values could be relevant for a lot of applications 
but there might be some exotic applications out there that would require their own assessment of what its critical 
values are.

| Impact Category  | Rank | Kolmogorov-Smirnov Distance boundary | Wasserstein Distance boundary | Possible Action |
|-----------|------|--------------------------------------|-------------------------------|-----------------|
| Negligible difference | S | 0.080 | 0.030 | No action required |
| Very Low | A | 0.150 | 0.060 | No action required |
| Low | B | 0.180 | 0.100 | Go for release create minor defect (or halt) |
| Medium | C | 0.220 | 0.125 | Halt release and create defect |
| High | D | 0.260 | 0.150 | Halt release and create defect |
| Very High | E | 0.300 | 0.200 | Halt release and create defect |
| Ultra | F | 0.340 | 0.250 | Halt release and create defect |

> When reading this table keep in mind that both statistics need fall in the same category if this is not the case
> the lowest category is selected.

For myself, I would only want an automated release to happen when the values the rank at least comes back as an **A** 
but this is my preference your organization could also want to for example release automatically on a **B** rank and 
figure out later what the problem is accepting the risk that a low-performance degradation will happen in production.

To see how drastically the CDF curves need to change for a rank to change you can view the animation below to get 
a better understanding of what the rank would roll out of our heuristic:

<!-- Ranking Animation-->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/ranking_simulation.gif?raw=true"/>
</p>

It is interesting to see that this ranking heuristic can filter out a test that is different from the baseline but what 
happens when there is no interesting change between two runs? For that, we would need a couple of constant 
test results sets which we can compare. For this reason, I have created the following ten example tests that contain a 
normal amount of difference to each other as you can tell from the image below:

<!-- Stable test runs -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-004.png?raw=true"/>
</p>

When these test are compared in the following order and pulled through our ranking 
heuristic we would get the following results:

| Baseline RunID | Benchmark RunID | Rank | Score | Kolmogorov-Smirnov Distance | Wasserstein Distance |
|----------------|-----------------|------|-------|-----------------------------|----------------------|
| RID-1 | RID-2 | S | 99.79 | 0.037 | 0.012 |
| RID-2 | RID-3 | S | 99.39 | 0.041 | 0.018 |
| RID-3 | RID-4 | S | 98.48 | 0.061 | 0.025 |
| RID-4 | RID-5 | S | 99.89 | 0.024 | 0.008 |
| RID-5 | RID-6 | A | 95.19 | 0.095 | 0.034 |
| RID-6 | RID-7 | S | 97.99 | 0.078 | 0.024 |
| RID-8 | RID-9 | S | 99.79 | 0.030 | 0.013 |
| RID-9 | RID-10 | S | 99.79 |0.016 | 0.014 |
 |
> You can run this experiment also for yourself by executing the following 
> [script from this project](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/simulations/simulate__with_always_stable_tests_results_no_regression.py).

In the previous example we tested test results that contain no change but how our ranking heuristic would react to a 
more drastic change can also be tested similarly. For this, we could use my favorite data set that contains a lot of 
different scenarios. You can interpret these results as different release moments where the release had a positive 
impact, a negative impact, and no impact below you can see the data set:

<!-- Example raw data scatter plot -->
<p align="center">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/raw-data-scatter-plot_raw-performance-test-data-001.png?raw=true"/>
</p>

When we also automatically analyze this data using our ranking heuristic we are left with the following results:

| Baseline RunID | Benchmark RunID | Rank | Score | Kolmogorov-Smirnov Distance | Wasserstein Distance |
|----------------|-----------------|------|-------|-----------------------------|----------------------|
| RID-1 | RID-2 | C | 74.4 |0.109 | 0.109 |
| RID-2 | RID-3 | S | 98.78 |0.067 | 0.020 |
| RID-3 | RID-4 | A | 91.87 |0.114 | 0.042 |
| RID-4 | RID-5 | A | 97.05 |0.047 | 0.041 |
| RID-5 | RID-6 | F | 0.000 |0.285 | 0.254 |

> You can find the source code for this experiment also in the following 
> [file in the project](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/simulations/simulate__with_always_unstable_tests_results_release_situation.py).

When correlating the  rank to what we see in our scatter plot we can determine that each score justified as 
**RID-2 to RID-5** are very similar in performance but have a low amount of difference one could accept as the amount of
distance is small, and it would therefore not directly impact our user experience.

## Contribute to this project 

Help me to make result analysis easier for more performance engineers around the globe by donating your 
expertise and knowledge, [anonymized test data](https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/data/contributing_data.md), 
or just by sharing this project on your socials together we can make this project smarter and more robust!

Feel free to open up an issue if you have any questions or are experiencing issues. **Want to contribute?** Then 
shoot in a pull request with your changes or test data, so we can continue to make improvements to this project. 

## Resources I found while learning about this topic

- [An article from data dog about selecting statistical distance for machine learning.](https://www.datadoghq.com/blog/engineering/robust-statistical-distances-for-machine-learning/)
- [How to read empirical cumulative distribution functions.](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480)
- [Performance Testing: Act like a detective. Use Raw Data! By Stijn Schepers](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) 
- [Stijn Schepers about raw data @ the Performance Advisory Council 2020](https://www.youtube.com/watch?v=TOYo5nIs7KE&list=PLdITSV_zl58qdb6fXZTqbsdE-j6h9J2gA&index=9)
___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/issues">- Open a issue</a> -
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/texts/contributing_data.md"> Share your raw data</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>
