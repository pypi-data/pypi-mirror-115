from typing import Sequence, List, Optional, Tuple, Any, Dict, NamedTuple
import plotly
import plotly.graph_objs as go
import numpy as np


# Legacy Invocation
# plotly.offline.init_notebook_mode()  # run at the start of every notebook

class EZPlotlyPlot(NamedTuple):
    plot_type: str
    title: Optional[str]
    xlabel: Optional[str]
    ylabel: Optional[str]
    plot_obj: Any
    xlim: Optional[List[float]]
    ylim: Optional[List[float]]
    xscale: Optional[str]
    yscale: Optional[str]
    x_dtick: Optional[float]
    y_dtick: Optional[float]


def hist(data: Sequence[float], min_bin: Optional[float] = None, max_bin: Optional[float] = None,
         bin_size: Optional[float] = None, histnorm: Optional[str] = None, title: Optional[str] = None,
         name: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
         color: Optional[str] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
         x_dtick: Optional[float] = None, y_dtick: Optional[float] = None,
         xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None) -> EZPlotlyPlot:
    """
    Makes a 1-D histogram of data.

    :param data: The data to plot as `Sequence[float]`
    :param min_bin: The left bin edge of the histogram as `Optional[float]`
    :param max_bin: The right bin edge of the histogram as `Optional[float]`
    :param bin_size: The size of a histogram bin as `Optional[float]`
    :param histnorm: The normalization scheme to use as `Optional[str]`
    :param title: Plot title as `Optional[str]`
    :param name: The name of the histogram as `str` (useful for plotting a series of histograms)
    :param xlabel: The x-axis label as `Optional[str]`
    :param ylabel: The y-axis label as `Optional[str]`
    :param color: The color of the histogram as `Optional[str]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :return:
        EZPlotlyPlot object representing histogram
    """

    # plot type
    plot_type = 'histogram'

    # y-label auto-setting
    if ylabel is None:
        if histnorm == 'probability':
            ylabel = 'Probability'
        else:
            ylabel = 'Frequency'
        if yscale == 'log':
            ylabel = 'log ' + ylabel

    # xbin properties
    if min_bin is None or max_bin is None or bin_size is None:
        xbins = None
    else:
        if xlim is None:
            xlim = [min_bin, max_bin]
        xbins = dict(start=min_bin, end=max_bin, size=bin_size)

    # assemble marker properties
    marker = dict()
    if color is not None:
        marker['color'] = color

    # assemble hist object
    hist_obj = go.Histogram(
        x=data,
        name=name,
        xbins=xbins,
        marker=marker,
        histnorm=histnorm
    )

    # return plot
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=hist_obj,
                        xlim=xlim, ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def bar(y: Sequence[float], x: Sequence[str] = (), error_y: Optional[Sequence[float]] = None,
        title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
        xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None,
        name: Optional[str] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
        x_dtick: Optional[float] = None, y_dtick: Optional[float] = None, text: Optional[str] = None,
        textposition: Optional[int] = None, color: Optional[str] = None) -> EZPlotlyPlot:
    """
    Makes a 1-D bar plot.

    :param y: The data for x-axis values as `Sequence[float]`
    :param x: The x-axis bar labels as `Sequence[str]`
    :param error_y: Error bar values as `Optional[Sequence[float]]`
    :param title: Plot title as `Optional[str]`
    :param xlabel: X-axis label as `Optional[str]`
    :param ylabel: Y-axis label as `Optional[str]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param name: The name of the bar plot as `Optional[str]` (useful if plotting a series of bar plots)
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :param text: Bar text as `Optional[str]`
    :param textposition:  Bar text position as `Optional[int]`
    :param color: The color of the bar series as `Optional[str]`
    :return:
        EZPlotlyPlot object represent bar chart
    """

    # plot type
    plot_type = 'bar'

    # define x range
    if len(x) == 0:
        x = [a for a in range(0, len(y))]

    # assemble bar object
    bar_obj = go.Bar(
        name=name,
        x=x,
        y=y,
        error_y=dict(
            type='data',
            array=error_y,
            visible=True
        ),
        text=text,
        textposition=textposition,
        marker_color=color
    )

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=bar_obj,
                        xlim=xlim, ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def scatter(x: Sequence[float], y: Sequence[float], error_y: Optional[Sequence[float]] = None,
            title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
            xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None,
            marker_size: Optional[float] = None, marker_color: Optional[str] = None, name: Optional[str] = None,
            point_anno: Optional[List[str]] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
            x_dtick: Optional[float] = None, y_dtick: Optional[float] = None) -> EZPlotlyPlot:
    """
    Makes a scatter plot.

    :param x: The x-data to plot as `Sequence[float]`
    :param y: The y-data to plot as `Sequence[float]`
    :param error_y: Error bar length as Sequence[float]`
    :param title: Plot title as `Optional[str]`
    :param xlabel: X-axis label as `Optional[str]`
    :param ylabel: Y-axis label as `Optional[str]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param marker_size: The size of a marker as `Optional[float]`
    :param marker_color: The color of a marker as `Optional[str]`
    :param name: The name of the scatter plot as `Optional[str]` (useful for plotting series)
    :param point_anno: Text annotations for each point as `Optional[List[str]]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :return:
        EZPlotlyPlot representing scatter plot
    """

    # plot type
    plot_type = 'scatter'

    # assemble marker information
    marker = dict()
    if marker_size is not None:
        marker['size'] = marker_size
    if marker_color is not None:
        marker['color'] = marker_color
    marker['type'] = 'circle'

    # make scatter gl object
    scatter_obj = go.Scatter(
        name=name,
        x=x,
        y=y,
        mode='markers',
        visible=True,
        marker=marker,
        text=point_anno,
        error_y=dict(
            type='data',
            array=error_y,
            visible=True
        )
    )

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=scatter_obj, xlim=xlim,
                        ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def scattergl(x: Sequence[float], y: Sequence[float], error_y: Optional[Sequence[float]] = None,
              title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
              xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None,
              marker_size: Optional[float] = None, marker_color: Optional[str] = None, name: Optional[str] = None,
              point_anno: Optional[List[str]] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
              x_dtick: Optional[float] = None, y_dtick: Optional[float] = None) -> EZPlotlyPlot:
    """
    Makes a scatter plot using open-gl backend.

    :param x: The x-data to plot as `Sequence[float]`
    :param y: The y-data to plot as `Sequence[float]`
    :param error_y: Error bar lengths as Sequence[float]`
    :param title: Plot title as `Optional[str]`
    :param xlabel: X-axis label as `Optional[str]`
    :param ylabel: Y-axis label as `Optional[str]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param marker_size: The size of a marker as `Optional[float]`
    :param marker_color: The color of a marker as `Optional[str]`
    :param name: The name of the scatter plot as `Optional[str]` (useful for plotting series)
    :param point_anno: Text annotations for each point as `Optional[List[str]]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as 'Optiona[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :return:
        EZPlotlyPlot object representing scatter plot
    """

    # plot type
    plot_type = 'scattergl'

    # assemble marker information
    marker = dict()
    if marker_size is not None:
        marker['size'] = marker_size
    if marker_color is not None:
        marker['color'] = marker_color

    # make scatter gl object
    error_y_dict = None
    if error_y is not None:
        error_y_dict = dict(type='data', array=error_y, visible=True)
    scatter_obj = go.Scattergl(
        name=name,
        x=x,
        y=y,
        mode='markers',
        visible=True,
        marker=marker,
        text=point_anno,
        error_y=error_y_dict
    )

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=scatter_obj,
                        xlim=xlim, ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def line(x: Sequence[float], y: Sequence[float], error_y: Optional[Sequence[float]] = None,
         lcl: Optional[Sequence[float]] = None, ucl: Optional[Sequence[float]] = None, title: Optional[str] = None,
         xlabel: Optional[str] = None, ylabel: Optional[str] = None, xlim: Optional[List[float]] = None,
         ylim: Optional[List[float]] = None, width: Optional[float] = None, color: Optional[str] = None,
         name: Optional[str] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
         x_dtick: Optional[float] = None, y_dtick: Optional[float] = None, dash: Optional[str] = None) -> EZPlotlyPlot:
    """
    Make line plot. Allows addition of confidence intervals specifying either uniform (via error_y)
    or non-uniform error bars (using lcl, ucl parameters).

    :param x: x-data as `Sequence[float]`
    :param y: y-data as `Sequence[float]`
    :param error_y: Error bar lengths as `Optional[Sequence[float]]`
    :param lcl: Lower confidence limits as `Optional[Sequence[float]]`
    :param ucl: Upper confidence limits as `Optional[Sequence[float]]`
    :param title: Plot title as `Optional[str]`
    :param xlabel: The x-axis label as `Optional[str]`
    :param ylabel: The y-axis label as `Optional[str]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param width: The width of the line as 'Optional[float]`
    :param color: The color of the line as `Optional[str]`
    :param name: The name of the line plot as `Optional[str]` (useful for plotting as series)
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[float]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[float]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :param dash: The dash type as `Optional[str]`
    :return:
        EZPlotlyPlot object representing line plot
    """

    # plot type
    plot_type = 'line'

    # assemble line information
    line_dict = dict()
    if width is not None:
        line_dict['width'] = width
    if color is not None:
        line_dict['color'] = color
    if dash is not None:
        line_dict['dash'] = dash
    if lcl is not None and ucl is not None:
        error_y_dict = dict(
            type='data',
            symmetric=False,
            array=ucl,
            arrayminus=lcl,
            visible=True
        )
    elif error_y is not None:
        error_y_dict = dict(
            type='data',
            array=error_y,
            visible=True
        )
    else:
        error_y_dict = None

    # make scatter object
    scatter_obj = go.Scattergl(
        name=name,
        x=x,
        y=y,
        error_y=error_y_dict,
        line=line_dict
    )

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=scatter_obj, xlim=xlim,
                        ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def violin(y: Sequence[float], title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
           name: Optional[str] = None, xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None,
           xscale: Optional[List[float]] = None, yscale: Optional[List[float]] = None,
           x_dtick: Optional[float] = None, y_dtick: Optional[float] = None) -> EZPlotlyPlot:
    """
    Make a single violin plot.

    :param y: The data for the violin plot as `Sequence[float]`
    :param title:  The title of the plot as `Optional[str]`
    :param xlabel: The x-axis label as `Optional[str]`
    :param ylabel: The y-axis label as `Optional[str]`
    :param name: The name of the violin plot as `Optional[str]` (useful for plotting series)
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :return:
        ezplotly Plot object representing violin plot
    """

    # plot type
    plot_type = 'violin'

    # make violin object
    violin_obj = go.Violin(
        y=y,
        name=name
    )

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=violin_obj, xlim=xlim,
                        ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def scatterheat(x: Sequence[float], y: Sequence[float], xbins: Sequence[float], ybins: Sequence[float],
                zscale: str = 'linear', title: Optional[str] = None, xlabel: Optional[str] = None,
                ylabel: Optional[str] = None, name: Optional[str] = None, xlim: Optional[List[float]] = None,
                ylim: Optional[List[float]] = None, xscale: Optional[str] = None, yscale: Optional[str] = None,
                x_dtick: Optional[float] = None, y_dtick: Optional[float] = None, cscale: Optional[List[float]] = None,
                outfile: Optional[str] = None, plot: bool = True) -> Optional[List[EZPlotlyPlot]]:
    """
    Plots a scatterplot and density heatmap side-by-side.

    :param x: The x-axis data as `Sequence[float]`
    :param y: The y-axis data as `Sequence[float]`
    :param xbins: x-axis bin edges for density heatmap as `Sequence[float]`
    :param ybins: y-axis bin edges for density heatmap as `Sequence[float]`
    :param zscale: The scale of the frequence dimension ('log', 'linear') as `str`
    :param title: Plot title as `Optional[str]`
    :param xlabel: The x-axis label as `Optional[str]`
    :param ylabel: The y-axis label as `Optional[str]`
    :param name: Name of plot as `str`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :param cscale: The color scale for heatmap [c_lower_lim, c_upper_lim] as `Optional[List[float]]`
    :param outfile: If specified, save to this file as `Optional[str]`
    :param plot: Whether to plot right now or suppress plot and return the plot object
        for downstream plotting by the user as `bool`
    :return:
        List[EZPlotlyPlot] representing figure set (if plot=False)
    """

    # transform data using np histogram
    z = np.histogram2d(x=y, y=x, bins=[ybins, xbins])[0]
    xlabels = xbins
    ylabels = ybins

    # transform data
    if zscale == 'log':
        z = np.log10(z)

    # return plots
    figs = list()
    figs.append(scattergl(x, y, xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim, xscale=xscale, yscale=yscale,
                          x_dtick=x_dtick, y_dtick=y_dtick, name=name, marker_size=5))
    figs.append(heatmap(z=z, xlabels=xlabels, ylabels=ylabels, xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim,
                        xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick, cscale=cscale))
    if plot:
        plot_all(figs, title=title, outfile=outfile)
    else:
        return figs


def heatmap(z: Sequence[Sequence[float]], xlabels: Sequence[Any] = None, ylabels: Sequence[Any] = None,
            title: Optional[str] = None, xlabel: Optional[str] = None, ylabel: Optional[str] = None,
            xlim: Optional[List[float]] = None, ylim: Optional[List[float]] = None, xscale: Optional[str] = None,
            yscale: Optional[str] = None, x_dtick: Optional[float] = None, y_dtick: Optional[float] = None,
            cscale: Optional[List[float]] = None, showcscale: bool = True) -> EZPlotlyPlot:
    """
    Plot heatmap

    :param z: 2-D heatmap as `Sequence[Sequence[float]]`
    :param xlabels: The xlabels as `Sequence[Any]`
    :param ylabels: The ylabels as `Sequence[Any]`
    :param title: The title of the heatmap as `Optional[str]`
    :param xlabel: The x-axis label as `Optional[str]`
    :param ylabel: The y-axis label as `Optional[str]`
    :param xlim: The x-axis limits [x_left_lim, x_right_lim] as `Optional[List[float]]`
    :param ylim: The y-axis limits [y_left_lim, y_right_lim] as `Optional[List[float]]`
    :param xscale: The scale of the x-axis ('log', 'linear') as `Optional[str]`
    :param yscale: The scale of the y-axis ('log', 'linear') as `Optional[str]`
    :param x_dtick: The plotting delta tick (i.e. tick length) of the x-axis as `Optional[float]`
    :param y_dtick: The plotting delta tick (i.e. tick length) of the y-axis as `Optional[float]`
    :param cscale: The color scale for heatmap [c_lower_lim, c_upper_lim] as `Optional[List[float]]`
    :param showcscale: Whether to show the color scale or not as `bool`
    :return:
        EZPlotlyPlot object representing heatmap
    """

    # plot type
    plot_type = 'heatmap'

    # color scale
    if cscale is None:
        zmin = None
        zmax = None
    else:
        zmin = cscale[0]
        zmax = cscale[1]

    # make heatmap object
    heatmap_obj = go.Heatmap(z=z, x=xlabels, y=ylabels, zmin=zmin, zmax=zmax, showscale=showcscale)

    # return
    return EZPlotlyPlot(plot_type=plot_type, title=title, xlabel=xlabel, ylabel=ylabel, plot_obj=heatmap_obj, xlim=xlim,
                        ylim=ylim, xscale=xscale, yscale=yscale, x_dtick=x_dtick, y_dtick=y_dtick)


def show(fig: Any) -> None:
    """
    Plots a single figure.

    :param fig: The figure to plot.
    :return:
    """
    plotly.offline.iplot(fig, filename='Subplot')


def extract_panel_title_positions(fig: Any) -> Dict[Any, Any]:
    title_annotations = list(fig['layout']['annotations'])
    return {t['text']: (t['x'], t['y']) for t in title_annotations}


def plot_all(plots: List[EZPlotlyPlot], panels: Optional[List[int]] = None, height: Optional[int] = None,
             width: Optional[int] = None, withhold: Optional[bool] = False,
             numcols: int = 1, title: Optional[str] = None, showlegend: bool = False,
             chrpacked: bool = False, outfile: Optional[str] = None, suppress_output: bool = False) -> Optional[Any]:
    """
    Global plotting function.

    :param plots: The plots to plot as `List[EZPlotlyPlot]`
    :param panels: A list of ints indicating which panel each plot goes into (if multiple panels) as
        `Optional[List[int]]`
    :param height: The height of the plotting area as `Optional[int]`
    :param width: The width of the plotting area as `Optional[int]`
    :param withhold: Whether to withhold the plot or plot right away as `bool`
    :param numcols: The number of panel columns per plotting row as `int`
    :param title: The title of the overall plot as `Optional[str]`
    :param showlegend: Whether to show the plot legends as `bool`
    :param chrpacked: Whether the plots are chrpacked (useful for bio chromosome plots) as `bool`
    :param outfile: The file to write the plot to as `Optional[str]`
    :param suppress_output: Whether to suppress output or not as `bool`
    :return:
        Base Plotly figure representing plot
    """

    # compute num panels needed to display everything
    if panels is None:
        num_panels = len(plots)
        panels = range(1, len(plots) + 1)
    else:
        num_panels = np.max(panels)

    # determine layout of Nx2 grid and adjust sizing
    num_rows = int(np.ceil(num_panels / numcols))
    if height is None:
        if chrpacked:
            height = num_rows * 200
        else:
            height = num_rows * 300
    if width is None:
        if chrpacked:
            width = numcols * 200
        else:
            width = 1000

    # extract panel titles
    panel_titles = ['' for _ in range(0, num_panels)]
    for plot_index in range(0, len(plots)):
        p = plots[plot_index]
        plot_title = p[1]
        panel_index = panels[plot_index]
        if plot_title is not None:
            panel_titles[panel_index - 1] = plot_title

    # make overall figure
    fig = plotly.subplots.make_subplots(rows=num_rows, cols=numcols, subplot_titles=panel_titles, print_grid=False)
    title_positions = extract_panel_title_positions(fig)

    # loop over plot generation
    for plot_index in range(0, len(plots)):

        # property extraction
        panel_index = panels[plot_index]
        p = plots[plot_index]
        plot_title = p.title
        xlabel = p.xlabel
        ylabel = p.ylabel
        plot = p.plot_obj
        xlim = p.xlim
        ylim = p.ylim
        xscale = p.xscale
        yscale = p.yscale
        x_dtick = p.x_dtick
        y_dtick = p.y_dtick

        # row/col
        row_index = int((panel_index - 1) / numcols + 1)
        col_index = int((panel_index - 1) % numcols + 1)

        # set up axis for figure
        fig.append_trace(plot, row_index, col_index)
        fig['layout']['xaxis' + str(panel_index)].update(showgrid=True)
        fig['layout']['yaxis' + str(panel_index)].update(showgrid=True)

        # redo figure axis labels for chrPacked=True
        if chrpacked:
            if col_index != 1:
                ylabel = None
            if xlabel is not None:
                new_anno = dict(
                    text=xlabel,
                    x=title_positions[plot_title][0],
                    xanchor='center',
                    xref='paper',
                    y=-0.043 + (num_rows - row_index) * 0.22,
                    yanchor='bottom',
                    yref='paper',
                    showarrow=False,
                    font=dict(size=14)
                )
                fig['layout']['annotations'] += (new_anno,)

        # set figure labels
        if xlabel is not None and not chrpacked:
            fig['layout']['xaxis' + str(panel_index)].update(title=xlabel)
        if ylabel is not None:
            fig['layout']['yaxis' + str(panel_index)].update(title=ylabel)
        if xscale is not None:
            fig['layout']['xaxis' + str(panel_index)].update(type=xscale)
        if yscale is not None:
            fig['layout']['yaxis' + str(panel_index)].update(type=yscale)
        if x_dtick is not None:
            fig['layout']['xaxis' + str(panel_index)].update(dtick=x_dtick)
        if y_dtick is not None:
            fig['layout']['yaxis' + str(panel_index)].update(dtick=y_dtick)
        if xlim is not None:
            fig['layout']['xaxis' + str(panel_index)].update(range=xlim, autorange=False, tick0=xlim[0])
        if ylim is not None:
            fig['layout']['yaxis' + str(panel_index)].update(range=ylim, autorange=False, tick0=ylim[0])

    # set overall layout and either withold plot or display it
    fig['layout'].update(height=height, width=width, showlegend=showlegend, title=title)
    if withhold:  # return fig (if additional custom changes need to be made)
        return fig
    else:
        if not suppress_output:
            plotly.offline.iplot(fig, filename='Subplot')
        if outfile is not None:
            plotly.io.write_image(fig, file=outfile)
