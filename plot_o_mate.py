#!/usr/bin/env python
"""
A command-line tool for plotting data with optional linear fitting and rolling averages.
"""

import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.stats import linregress


def get_args():
    """
    Parse and return command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Plot data with optional linear fitting and rolling averages.")
    
    # Required arguments
    parser.add_argument(
        "filename",
        nargs="+",
        help="Input file(s) containing the data to plot."
    )
    
    # Optional arguments
    parser.add_argument(
        "-pn", "--plot_name",
        type=str,
        default=None,
        help="Custom name for the plot and title."
    )
    parser.add_argument(
        "-pl", "--plot_labels",
        nargs="+",
        default=None,
        help="Custom labels for the plot curves."
    )
    parser.add_argument(
        "-ra", "--rolling_average",
        type=int,
        default=1,
        help="Window size for rolling average (default: 1, no rolling average)."
    )
    parser.add_argument(
        "-x", "--x_axis_label",
        type=str,
        default=None,
        help="Label for the x-axis."
    )
    parser.add_argument(
        "-x_high", "--x_axis_high_lim",
        type=float,
        default=None,
        help="Upper limit for the x-axis."
    )
    parser.add_argument(
        "-x_low", "--x_axis_low_lim",
        type=float,
        default=None,
        help="Lower limit for the x-axis."
    )
    parser.add_argument(
        "-y", "--y_axis_label",
        type=str,
        default=None,
        help="Label for the y-axis."
    )
    parser.add_argument(
        "-y_high", "--y_axis_high_lim",
        type=float,
        default=None,
        help="Upper limit for the y-axis."
    )
    parser.add_argument(
        "-y_low", "--y_axis_low_lim",
        type=float,
        default=None,
        help="Lower limit for the y-axis."
    )
    parser.add_argument(
        "-fc", "--factor_conversion",
        type=float,
        default=1,
        help="Factor to convert y-values by."
    )
    parser.add_argument(
        "-fx", "--x_axis_conversion",
        type=float,
        default=1,
        help="Factor to scale the x-axis by."
    )
    parser.add_argument(
        "-lc", "--line_colors",
        nargs="+",
        default=None,
        help="Colors for the plot curves."
    )
    parser.add_argument(
        "-ls", "--line_styles",
        nargs="+",
        default=None,
        help="Line styles for the plot curves."
    )
    parser.add_argument(
        "-mk", "--markers",
        nargs="+",
        default=None,
        help="Markers for the plot curves."
    )
    parser.add_argument(
        "-fit", "--fit_type",
        type=str,
        default=None,
        help="Type of fit to apply (e.g., 'linear')."
    )
    parser.add_argument(
        "-sd", "--stdev",
        type=int,
        default=None,
        help="Index of the column containing standard deviation values."
    )
    parser.add_argument(
        "-fs", "--fontsize",
        type=int,
        default=None,
        help="Font size for the plot elements."
    )
    
    return parser.parse_args()


def make_table(filename, stdev_index=None):
    """
    Read data from a file and return it as a list of lists.

    Args:
        filename (str): Path to the input file.
        stdev_index (int, optional): Index of the column containing standard deviation values.

    Returns:
        list: A list containing x-values, y-values, and optionally standard deviations.
    """
    data = [[], [], [] if stdev_index is not None else None]  # Additional list for standard deviation
    
    with open(filename, "r") as file:
        for line in file:
            if not line.startswith(("#", "@")):
                columns = line.split()
                step = float(columns[0])
                energy = float(columns[1])
                data[0].append(step)
                data[1].append(energy)
                if stdev_index is not None and stdev_index < len(columns):
                    data[2].append(float(columns[stdev_index]))
    
    return data


def make_plot(table, label, rolling_average, color=None, style=None, marker=None, fit_type=None, fontsize=None):
    """
    Plot the data with optional rolling average, fit, and styling.

    Args:
        table (list): Data to plot (x-values, y-values, and optionally standard deviations).
        label (str): Label for the plot curve.
        rolling_average (int): Window size for rolling average.
        color (str, optional): Color for the plot curve.
        style (str, optional): Line style for the plot curve.
        marker (str, optional): Marker for the plot curve.
        fit_type (str, optional): Type of fit to apply (e.g., 'linear').
        fontsize (int, optional): Font size for the plot elements.
    """
    x_values = np.array([x * arguments.x_axis_conversion for x in table[0]])
    y_values = np.array([y * arguments.factor_conversion for y in table[1]])

    # Apply rolling average if requested
    if rolling_average > 1:
        y_values = np.convolve(y_values, np.ones(rolling_average) / rolling_average, mode="valid")
        x_values = x_values[:len(y_values)]

    # Plot the data
    plt.plot(x_values, y_values, label=label, color=color, linestyle=style if fit_type is None else "", marker=marker)

    # Plot shaded area for standard deviation if provided
    if table[2] is not None:
        std_values = np.array(table[2])
        if rolling_average > 1:
            std_values = np.convolve(std_values, np.ones(rolling_average) / rolling_average, mode="valid")
        plt.fill_between(x_values, y_values - std_values, y_values + std_values, color=color, alpha=0.3)

    # Add linear fit if requested
    if fit_type == "linear":
        slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
        fit_line = slope * x_values + intercept
        plt.plot(x_values, fit_line, label=f"{label} (fit)", color=color, linestyle="--")

    # Customize plot appearance
    if arguments.plot_name:
        plt.title(arguments.plot_name, fontsize=fontsize)
    if arguments.x_axis_label:
        plt.xlabel(arguments.x_axis_label, fontsize=fontsize)
    if arguments.y_axis_label:
        plt.ylabel(arguments.y_axis_label, fontsize=fontsize)
    
    plt.tick_params(labelsize=fontsize)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)


def save_plot(plotname):
    """
    Save the plot to a file.

    Args:
        plotname (str): Base name for the output file.
    """
    plt.savefig(f"{plotname}.pdf", transparent=True)


if __name__ == "__main__":
    arguments = get_args()
    
    for n, filename in enumerate(arguments.filename):
        label = arguments.plot_labels[n] if arguments.plot_labels else None
        color = arguments.line_colors[n] if arguments.line_colors else None
        style = arguments.line_styles[n] if arguments.line_styles else None
        marker = arguments.markers[n] if arguments.markers else None
        fontsize = arguments.fontsize if arguments.fontsize else None
        
        data_table = make_table(filename, stdev_index=arguments.stdev)
        make_plot(data_table, label=label, rolling_average=arguments.rolling_average,
                  color=color, style=style, marker=marker, fit_type=arguments.fit_type, fontsize=fontsize)
    
    # Finalize and save the plot
    plotname = arguments.plot_name if arguments.plot_name else arguments.filename[0][:-4]
    if arguments.x_axis_low_lim or arguments.x_axis_high_lim:
        plt.xlim(arguments.x_axis_low_lim, arguments.x_axis_high_lim)
    if arguments.y_axis_low_lim or arguments.y_axis_high_lim:
        plt.ylim(arguments.y_axis_low_lim, arguments.y_axis_high_lim)
    
    plt.tight_layout()
    plt.legend()
    save_plot(plotname)