#!/usr/bin/env python
from ast import arg
import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.stats import linregress

def get_args():
    'get the command line arguments for the plot raw data'
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        action='store',
                        nargs='+')
    parser.add_argument("-pn", "--plot_name",
                        type=str,
                        default=None,
                        help='custom name for plot and title')
    parser.add_argument("-pl", "--plot_labels",
                        action='store',
                        default=None,
                        help='custom labels for plot curves',
                        nargs='+')
    parser.add_argument("-ra", "--rolling_average",
                        type=int,
                        default=1,
                        help='window size for rolling average (default: 1, i.e., no rolling average)')
    parser.add_argument("-x", "--x_axis_label",
                        type=str,
                        default=None,
                        help='x axis label for the plot(s))')
    parser.add_argument("-x_high", "--x_axis_high_lim",
                        type=float,
                        default=None,
                        help='x axis bounds lower limit boundary for the plot')
    parser.add_argument("-x_low", "--x_axis_low_lim",
                        type=float,
                        default=None,
                        help='x axis bounds higher limit boundary for the plot')
    parser.add_argument("-y", "--y_axis_label",
                        type=str,
                        default=None,
                        help='y axis label for the plot(s))')
    parser.add_argument("-y_high", "--y_axis_high_lim",
                        type=float,
                        default=None,
                        help='y axis bounds lower limit boundary for the plot')
    parser.add_argument("-y_low", "--y_axis_low_lim",
                        type=float,
                        default=None,
                        help='y axis bounds higher limit boundary for the plot')
    parser.add_argument("-fc", "--factor_conversion",
                        type=float,
                        default=1,
                        help='convert y values by some factor')
    parser.add_argument("-fx", "--x_axis_conversion",
                        type=float,
                        default=1,
                        help='scale x axis by some linear factor')
    parser.add_argument("-lc", "--line_colors",
                        type=str,
                        default=None,
                        help='line colors for the plot curves',
                        nargs='+')
    parser.add_argument("-ls", "--line_styles",
                        type=str,
                        default=None,
                        help='line styles for the plot curves',
                        nargs='+')
    parser.add_argument("-mk", "--markers",
                        type=str,
                        default=None,
                        help='markers for the plot curves',
                        nargs='+')
    parser.add_argument("-fit", "--fit_type",
                        type=str,
                        default=None,
                        help='fit type for the data ("linear" for linear fit)')
    parser.add_argument("-sd", "--stdev",
                            type=int,
                            default=None,
                            help='index of the column containing standard deviation values')
    parser.add_argument("-fs", "--fontsize",
                        type=int,
                        default=None,
                        help='Non-standard font size in use for everything')
    return parser.parse_args()

def make_table(filename, stdev_index=None):
    'strip the xvg file of all the initial comments and convert the tab-delimited columns of steps and energy into a list of tuples'
    optimisation = [[], [], [] if stdev_index is not None else None]  # Additional list for standard deviation
    with open(filename, 'r') as xvg:
        for line in xvg:
            if not line.startswith(('#', '@')):
                columns = line.split()
                step = float(columns[0])
                energy = float(columns[1])
                optimisation[0].append(step)
                optimisation[1].append(energy)
                if stdev_index is not None and stdev_index < len(columns):
                    optimisation[2].append(float(columns[stdev_index]))
    return optimisation

def make_plot(table, filename, label, rolling_average, color=None, style=None, marker=None, fit_type=None, fontsize=None):
    x_values = np.array([x*arguments.x_axis_conversion for x in table[0]])
    y_values = np.array([y*arguments.factor_conversion for y in table[1]])

    # Apply rolling average if requested
    if rolling_average > 1:
        y_values = np.convolve(y_values, np.ones(rolling_average)/rolling_average, mode='valid')
        x_values = x_values[:len(y_values)]

    # Plot the data with markers and without line style if fit is requested
    plt.plot(x_values, y_values, label=label, color=color, linestyle=style if fit_type is None else '', marker=marker)

    # Plot shaded area for standard deviation if provided
    if table[2] is not None:
        std_values = np.array(table[2])
        if rolling_average > 1:
            std_values = np.convolve(std_values, np.ones(rolling_average)/rolling_average, mode='valid')
        plt.fill_between(x_values, y_values - std_values, y_values + std_values, color=color, alpha=0.3)

    # Add linear fit if requested
    if fit_type == "linear":
        slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
        fit_line = slope * x_values + intercept
        plt.plot(x_values, fit_line, label=f"{label} (fit)", color=color, linestyle='--')

    if arguments.plot_name:
        plt.title(arguments.plot_name, fontsize=fontsize)
    else:
        plt.title(None, fontsize=fontsize)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
    if arguments.x_axis_label:
        plt.xlabel(arguments.x_axis_label, fontsize=fontsize)
    if arguments.y_axis_label:
        plt.ylabel(arguments.y_axis_label, fontsize=fontsize)
    
    plt.tick_params(labelsize=fontsize)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

def saveplot(plotname):
    plt.savefig(plotname+".pdf", transparent=True)

if __name__ == '__main__':
    arguments = get_args()
    for n, filename in enumerate(arguments.filename):
        label = arguments.plot_labels[n] if arguments.plot_labels else None
        color = arguments.line_colors[n] if arguments.line_colors else None
        style = arguments.line_styles[n] if arguments.line_styles else None
        marker = arguments.markers[n] if arguments.markers else None
        fontsize = arguments.fontsize if arguments.fontsize else None
        optimisation_table = make_table(filename, stdev_index=arguments.stdev)
        make_plot(optimisation_table, filename, label=label, rolling_average=arguments.rolling_average,
                  color=color, style=style, marker=marker, fit_type=arguments.fit_type, fontsize=fontsize)
        

    plotname = arguments.plot_name if arguments.plot_name else arguments.filename[0][:-4]
    if arguments.x_axis_low_lim or arguments.x_axis_high_lim:
        plt.xlim(arguments.x_axis_low_lim, arguments.x_axis_high_lim)
    if arguments.y_axis_low_lim or arguments.y_axis_high_lim:
        plt.ylim(arguments.y_axis_low_lim, arguments.y_axis_high_lim)
    plt.tight_layout()
    plt.legend()
    saveplot(plotname)
