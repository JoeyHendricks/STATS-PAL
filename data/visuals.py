from os.path import isfile, join
from os import listdir
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import imageio
import os


class LineGraph:

    def __init__(self, benchmark, baseline, wasserstein_distance, kolmogorov_smirnov_distance, rank, score, change):
        """
        Will build the image.
        :param benchmark:
        :param baseline:
        """
        benchmark["type"] = ["benchmark" for _ in range(0, len(benchmark["measure"]))]
        baseline["type"] = ["baseline" for _ in range(0, len(baseline["measure"]))]
        self.wasserstein_distance = wasserstein_distance
        self.kolmogorov_smirnov_distance = kolmogorov_smirnov_distance
        self.rank = rank
        self.score = score
        self.change = change
        self.dataframe = pd.concat([baseline, benchmark])
        self.message_versus_simulation = f"Wasserstein d-value <b>{self.wasserstein_distance}</b>, " \
                                         f"KS d-value: <b>{self.kolmogorov_smirnov_distance}</b>"
        self.message_estimated_rank_simulation = f" Estimated rank: <b>{self.rank}</b>"

    def _render_figure(self):
        """
        Will render the data into a figure.
        :return:
        """
        figure = px.line(self.dataframe, x="probability", y="measure", color='type')
        figure.add_annotation(
            dict(
                font=dict(color='black', size=15),
                x=0.5,
                y=-0.12,
                showarrow=False,
                text=self.message_versus_simulation + self.message_estimated_rank_simulation,
                textangle=0,
                align="center",
                xref="paper",
                yref="paper")
        )
        figure.update_layout(
            height=800,
            width=800,
            yaxis_range=[-1.1, 2.1],
            title_text=f'Benchmark Vs Baseline randomly introduced distance: <b>{self.change}</b>',
            title_x=0.5
        )
        return figure

    def show(self) -> None:
        """
        Will display the image in your default browser.
        """
        figure = self._render_figure()
        figure.show()

    def save_frame(self, folder: str, filename: str, image_format=".png") -> None:
        """
        Saving image using the orca engine the default
        kaleido engine was not working for me.
        :param image_format : The format of the image
        :param folder: target folder on disk
        :param filename: the file name;
        """
        figure = self._render_figure()
        if not os.path.exists(folder):
            os.mkdir(folder)

        figure.write_image(
            file=f"{str(folder)}\\{str(filename)}{str(image_format)}",
            format=image_format.strip("."),
            engine="orca"
        )


class ScatterPlot:

    def __init__(self, scenario, rank, score, change):
        """
        will build a scatter plot image
        :param scenario:
        :param rank:
        :param change:
        """
        self.scenario = scenario
        self.rank = rank
        self.score = score
        self.change = change

    def _render_figure(self):
        """
        Will render the data into a figure.
        :return:
        """
        figure = make_subplots(rows=1, cols=2)
        figure.add_trace(
            go.Scatter(x=self.scenario.benchmark_x, y=self.scenario.benchmark_y,
                       mode='markers', name="benchmark"
                       ),
            row=1,
            col=1
        )

        figure.add_trace(
            go.Scatter(x=self.scenario.baseline_x, y=self.scenario.baseline_y,
                       mode='markers', name="baseline"
                       ),
            row=1,
            col=2,
        )
        figure.update_layout(
            height=800, width=1200,
            title_text=f"Benchmark Vs Baseline, ranked: <b>{self.rank}</b>",
        )
        figure.update_yaxes(type="log", range=[-2.5, 2.5], title_text="Response Time in Seconds (logarithmic scale)")
        figure.update_xaxes(title_text="Epoch Time Stamps")
        return figure

    def show(self) -> None:
        """
        Will display the image in your default browser.
        """
        figure = self._render_figure()
        figure.show()

    def save_frame(self, folder: str, filename: str, image_format=".png") -> None:
        """
        Saving image using the orca engine the default
        kaleido engine was not working for me.
        :param image_format : The format of the image
        :param folder: target folder on disk
        :param filename: the file name;
        """
        figure = self._render_figure()
        if not os.path.exists(folder):
            os.mkdir(folder)

        figure.write_image(
            file=f"{str(folder)}\\{str(filename)}{str(image_format)}",
            format=image_format.strip("."),
            engine="orca"
        )


class Animation:

    def __init__(self):
        pass

    @staticmethod
    def render_frames_in_target_directory_to_gif(target_folder: str, export_folder: str):
        """
        Will create gif.
        :return:
        """
        images = []
        files_in_target_folder = [f for f in listdir(target_folder) if isfile(join(target_folder, f))]
        for file_name in files_in_target_folder:
            images.append(imageio.imread(f"{target_folder}\\{file_name}"))
        imageio.mimsave(f"{export_folder}\\out.gif", images)
