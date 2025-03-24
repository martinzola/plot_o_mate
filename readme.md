![Logo](images/logo.png)

# Plot_o_mate: An easy to use data plotting tool

This is a simple command-line program that allows a user to plot any simple two-column file(s) containing X and Y data,
with with optional transformations such as linear fitting and rolling averages. It supports custom labels, axis limits, and styling options.

## Features
- Plot data from one or more input files .txt, txt, and any other file format where the data is stored as text separated into columns.)
- Apply rolling averages to smooth data.
- Add linear fits to the data.
- Customize plot titles, axis labels, and styling (colors, line styles, markers).
- Save plots as PDF files.

## Installation

1. Clone this repository:  
   git clone https://github.com/martinzola/plotly

2. Install dependencies:  
    cd plotly  
    pip install -r requirements.txt  

3. *(Optional)* Make executable (in macOS and Linux):  
    chmod +x plot_o_mate.py  
    *This will mean that you do not have to prefix the plot_o_mate.py command with the python command*  

4. *(Optional)* Add to bin:  
    cp plot_o_mate.py path/to/your/bin  


## Basic Example

To plot data from a file data.txt:  
    python plot_o_mate.py data.txt  

*More examples can be found in the /examples directory, with detailed explanations of the different commands and*
*how they are used to customise the plots.* 

**NOTE**:*For each command, the full command name can be used, or the shorthand for it.*
*For example, the plot title can be specified using:*  
        -pt "plot title"  

        or  

        --plot_title "plot title"


## Customizing the Plot

Add a title and axis labels:
    python plot_data.py data.txt --plot_name "My Plot" --x_axis_label "Time (s)" --y_axis_label "Energy (kJ/mol)"

Apply a rolling average with a window size of 5:
    python plot_data.py data.txt --rolling_average 5

Add a linear fit:
    python plot_data.py data.txt --fit_type linear

Customize line colors, styles, and markers:
    python plot_data.py data.txt --line_colors red --line_styles dashed --markers o

Set axis limits:
    python plot_data.py data.txt --x_axis_low_lim 0 --x_axis_high_lim 10 --y_axis_low_lim -5 --y_axis_high_lim 5

## Multiple Files

To plot data from multiple files with custom labels:
    python plot_data.py data1.txt data2.txt --plot_labels "Dataset 1" "Dataset 2"
    
## Standard Deviation

If your data includes standard deviation values in a specific column (e.g., column 2):
    python plot_data.py data.txt --stdev 2

## Save the Plot

The plot is automatically saved as a PDF file. The default filename is derived from the input file name, but you can specify a custom name:
    python plot_data.py data.txt --plot_name "My Plot"

## Command-Line Arguments

Argument	    Description

filename	        Input file(s) containing the data to plot.

--plot_name 	    Custom name for the plot and title.

--plot_labels	    Custom labels for the plot curves (one per input file).

--rolling_average	Window size for rolling average (default: 1, no rolling average).

--x_axis_label	    Label for the x-axis.

--x_axis_high_lim	Upper limit for the x-axis.

--x_axis_low_lim	Lower limit for the x-axis.

--y_axis_label	    Label for the y-axis.

--y_axis_high_lim	Upper limit for the y-axis.

--y_axis_low_lim	Lower limit for the y-axis.

--factor_conversion	Factor to convert y-values by (default: 1).

--x_axis_conversion	Factor to scale the x-axis by (default: 1).

--line_colors	    Colors for the plot curves (one per input file).

--line_styles	    Line styles for the plot curves (one per input file).

--markers	        Markers for the plot curves (one per input file).

--fit_type	        Type of fit to apply (e.g., "linear").

--stdev	            Index of the column containing standard deviation values

--fontsize	        Font size for the plot elements.
