

Our beautiful digital world is changing faster every day and with increased speed comes unprecedented more demand for 
automating more complex actions so organizations can pick up speed and face our ever more demanding online world.

That is why there is nothing new for performance engineering experts to execute their tests continuously. However, 
when integrating their entire testing process into a pipeline we quickly recognize that the analysis of our complex 
test results is not an easy hurdle to overcome.

## Don’t bother me unless it is important

But what does it mean to analyze our test results automatically in a pipeline? In my opinion, it means that one 
wants to be able to trust an automatic analysis completely and only be prompted to look at test results when there 
is an interesting difference.

Otherwise, we would want to let it go to production without any manual intervention as our 
automated analysis has determined that there is no significant risk. 

## Keep it raw

When learning the ropes to become a performance engineer my mentor and good friend 
[Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) would always hammer in the importance of using raw data 
and, you know what the man is absolutely right.

> If you want to learn more about raw data I would recommend reading Stijn's 
> [work](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) 
> on the matter as he has covered this topic very extensively.

Raw data is a powerful tool that we have at our disposal to truly study how the system we are testing is acting, 
looking at the example below this becomes very evident when we look at an average line graph versus a raw scatter plot.

<!-- Raw Data Vs Averages animation -->
<p style="float: left;">
    <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>
</p>

*Keep in mind that both illustrations are from the same test* and that these results make it painstakingly clear 
that averages hide the actual behavior while the raw data show exactly what behavior or application has been portraying. 

Because of the magnificent detail, raw data presents us we would any automated decision-making to be based solely 
on the raw version of test results and not an aggregated or averaged out data set as this will make our calculation 
simply inaccurate. 

## 1.5 meters distance, please!

During this pandemic, you for sure have seen signs everywhere reminding you to keep your 
[distance](https://en.wikipedia.org/wiki/Statistical_distance)  from your fellow man. But what does 
[distance](https://en.wikipedia.org/wiki/Statistical_distance)  mean when we are analyzing our performance test 
results? In a sense, it implies that we would like to know how much difference there is between a baseline, and a 
completed benchmark test.

## The Wasserstein & Kolmogorov-Smirnov Distance

In the field of statistics, there are a lot of distance metrics that can indicate to us how much there is between 
two tests one of these metrics which is utterly great for our use case is the 
[Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric) the equation to calculate this metric goes 
as follows:

<!-- Wasserstein distance equation -->
<p style="float: left;">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/wasserstein_distance_equation.png"/>
</p>

For most people, this formula would like some ancient runic spell which makes it a bit daunting to start learning 
more about this metric. However, understanding this metric becomes a lot easier when we look at its physical example:

**Consider this, both your baseline and benchmark test results are piles of dirt. Your boss asks you to make the 
benchmark pile of dirt as large as the baseline pile. The amount of work or in other words the amount of dirt required 
to make both piles the same size is the Wasserstein Distance which is why it is also known as the 
[Earth Mover’s distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance).**

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


