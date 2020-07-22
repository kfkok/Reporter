import os
import pickle
import shutil
import numpy as np

import matplotlib.pyplot as plt


class Reporter(object):
    """A simple class that generates a results directory, collects the data(s) from client program,
    and plots graphs for each data channel. This class is designed using the facade design pattern
    that consists of static methods, therefore it can be decoupled easily from the client code.
    This class is particular useful to plot reinforcement learning model result graphs.
    """

    class Type:
        """The type of the plot"""
        PLOT = 0
        COUNT = 1

    directory = ""
    reports = []

    @staticmethod
    def create_results_directory(results_dir):
        """
        Generate a result directory in results_dir for the Reporter class to dump all of its output.

        :return: The created directory path is set as current working directory
        """

        # if os.path.exists(results_dir) and os.path.isdir(results_dir):
        #     shutil.rmtree(results_dir)

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        Reporter.directory = results_dir

        return results_dir

    @staticmethod
    def clear(*args):
        """
        Clear all the values for each variable
        :param args:
        :return:
        """
        reports = Reporter.get_reports(*args)

        for report in reports:
            report["value"].clear()

    @staticmethod
    def reset():
        """Delete all reports"""
        Reporter.reports = []

    @staticmethod
    def setup(name, xlabel, type="", **kwargs):
        """
        Setup a report so that data relevant to the report can be appended to it later.
        \n Also specifies the plot type required for this report (Default is standard plot).

        :param name: The report name
        :param xlabel: x-axis label for the report plot
        :param type: plot type, select from Reporter.Type
        :param kwargs:
        :return:
        """
        if len(Reporter.get_reports(name)) > 0:
            return

        # Default plot type set to PLOT if type is not specified
        type = Reporter.Type.PLOT if type == "" else type

        if type == Reporter.Type.PLOT:
            value = []
        elif type == Reporter.Type.COUNT:
            value = {}
        else:
            raise Exception("undefined report type", type)

        Reporter.reports.append({
            "name": name,
            "xlabel": xlabel,
            "type": type,
            "value": value,
        })

    @staticmethod
    def get_reports(*names):
        """
        Returns a list of reports that matches the report names, or return all reports if names is empty
        :param names:
        :return: list a reports that matches the report names or all reports if is empty
        """
        return [r for r in Reporter.reports if r["name"] in names] if len(names) > 0 else Reporter.reports

    @staticmethod
    def append(name, value):
        reports = Reporter.get_reports(name)
        if len(reports) == 0:
            ex = "report for " + name + " do not exist, setup it first before append"
            raise Exception(ex)

        report = reports[0]

        if report["type"] == Reporter.Type.PLOT:
            report["value"].append(value)
        elif report["type"] == Reporter.Type.COUNT:
            report["value"].setdefault(value, 0)
            report["value"][value] += 1
        else:
            raise Exception("undefined report type", report["type"])

    @staticmethod
    def save_figure(file, *names):
        plt.switch_backend('agg')
        plt.figure(figsize=(20, 10))
        plt.subplots_adjust(hspace=0.5)
        plt.title(file)

        # Collect the reports, single plot and multi plots
        reports = []

        if len(names) == 0:
            # get all reports if names not specified
            reports = Reporter.get_reports()
        else:
            for name in names:
                # multiple plots on same graph
                if type(name) == list:
                    # first element of name is the list of report names
                    report_names = name[0]
                    report_list = Reporter.get_reports(*report_names)
                    # second element of name is x_label, appended at the 2nd end of report list
                    # third element of name is y_label, appended at the end of report list
                    # report list = [[[report-1], [report-2], ... [report-n]], x_label, y_label]
                    report_list = [report_list, name[1], name[2]]
                # single plot
                else:
                    report_list = Reporter.get_reports(name)

                if len(report_list) == 0:
                    pass
                else:
                    reports.append(report_list if type(name) == list else report_list[0])

        # Process the reports
        for i in range(len(reports)):
            plt_index = str(len(reports)) + str(1) + str(i + 1)
            plt.subplot(plt_index)

            report = reports[i]

            # single plot
            if type(report) is dict:
                plt.ylabel(report["name"])
                plt.xlabel(report["xlabel"])

                Reporter.single_plot(report)

            # multi plots
            else:
                plt.ylabel(report[2])
                plt.xlabel(report[1])

                for r in report[0]:
                    Reporter.single_plot(r)

                plt.legend(loc='upper right')

        file = os.path.join(Reporter.directory, file)
        plt.savefig(file)
        print("figure saved in ", file)
        plt.close()

    @staticmethod
    def single_plot(report):
        if report["type"] == Reporter.Type.PLOT:
            plt.plot(report["value"], label=report["name"])
        elif report["type"] == Reporter.Type.COUNT:
            plt.bar(report["value"].keys(), report["value"].values())

    @staticmethod
    def dump_reports(*args):
        reports = Reporter.get_reports(*args)
        for report in reports:
            with open(Reporter.directory + report['name'] + '.pkl', 'wb') as handle:
                pickle.dump(report, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def dump_variable(file, variable):
        with open(Reporter.directory + file + '.pkl', 'wb') as handle:
            pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def plot_mean_variance(y, label, color, figure_num='', x_offset=0):
        # dimension check
        y = np.array(y)
        assert y.ndim == 2

        mean = y.mean(axis=0)
        error = y.std(axis=0)

        figure_num = plt.figure(figure_num)
        x = np.arange(y.shape[1]) + x_offset
        plt.plot(x, mean, color=color, label=label)
        plt.fill_between(x, mean - error, mean + error, facecolor=color, alpha=0.15)

        return figure_num

    @staticmethod
    def save_plot_comparison(file, plots, title, xlabel, ylabel):
        fig = plt.figure()
        plt.margins(x=0)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        total_subplots = len(plots)
        colors = ['b', 'r', 'g', 'k', 'c', 'm']

        if total_subplots > len(colors):
            raise Exception("maximum number of supported subplots is {}, got {} instead".format(len(colors),
                                                                                                total_subplots))

        for color, subplot in zip(colors, plots.items()):
            label = subplot[0]
            y = subplot[1]
            Reporter.plot_mean_variance(y, label, color, fig.number)

        plt.legend(loc='upper right')

        file = os.path.join(Reporter.directory, file)
        plt.savefig(file)
        print("figure saved in ", file)
        plt.close()

