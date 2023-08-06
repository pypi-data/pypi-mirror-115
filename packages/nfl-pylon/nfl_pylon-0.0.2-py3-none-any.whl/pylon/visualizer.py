# python 3.6
# basic data viz
# TODO: refactor some of the redundant code into subroutines
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# credits to Deryck97's python guide
TEAM_COLORS = {
	'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773', 'BUF': '#00338D', 'CAR': '#0085CA',
	'CHI': '#00143F', 'CIN': '#FB4F14', 'CLE': '#FB4F14', 'DAL': '#B0B7BC', 'DEN': '#002244',
	'DET': '#046EB4', 'GB': '#24423C', 'HOU': '#C9243F', 'IND': '#003D79', 'JAX': '#136677',
	'KC': '#CA2430', 'LA': '#002147', 'LAC': '#2072BA', 'LV': '#C4C9CC', 'MIA': '#0091A0',
	'MIN': '#4F2E84', 'NE': '#0A2342', 'NO': '#A08A58', 'NYG': '#192E6C', 'NYJ': '#203731',
	'PHI': '#014A53', 'PIT': '#FFC20E', 'SEA': '#7AC142', 'SF': '#C9243F', 'TB': '#D40909',
	'TEN': '#4095D1', 'WAS': '#FFC20F'
}


def __get_logos() -> list:
	filepath = "../../data/logos"
	logos = os.listdir(filepath)
	return [
		filepath + str(item)
		for item in logos
	]


def __get_image(path: str) -> OffsetImage:
	"""
	function to put images onto a plot.
	:param path: string path to the image
	:return: OffsetImage object
	"""
	# Full credits to
	# 	https://github.com/jezlax/sports_analytics/blob/9e327b2c5e078f84469c5cf8d41fb6e352cad38e/animated_nfl_scatter.py#L141
	# 	and Deryck97's nflfastR python guide for this code.
	return OffsetImage(plt.imread(path), zoom=0.5)


def build_histogram(x: pd.Series, **kwargs) -> (plt.Figure, plt.Axes):
	"""
	function to build a histogram for the distribution of a variable X
	:param x: variable whose distribution will be plotted
	:param kwargs: parameters to pass to build the graph.
	Args:
		figsize (tuple(int, int)): specify the size of the plot. defaults to (15, 15)
		best_fit (bool): if True, will plot a best-fit curve on the histogram. Defaults to False
		x_label (str): the title written to the x-axis. Defaults to 'X'
		y_label (str): the title written to the y-axis. Defaults to 'y'
		title (str): the title of the graph or plot. Defaults to 'title'
		save_as (str): the filename to which the function will attempt to save the generated plot. If None (default),
		no save will occur
	:return: tuple of (plt.Figure, plt.Axes) objects. This allows for additional customization to the plot and provides
	flexibility in the library
	"""
	if x.size <= 0:
		raise ValueError("Invalid arguments passed to function (build-histogram): size of input series is 0.")

	opts = {
		'figsize': (15, 15) if 'figsize' not in kwargs else kwargs['figsize'],
		'best_fit': False if 'best_fit' not in kwargs else kwargs['best_fit'],
		'x_label': 'X' if 'x_label' not in kwargs else str(kwargs['x_label']),
		'y_label': 'y' if 'y_label' not in kwargs else str(kwargs['y_label']),
		'title': 'Title' if 'title' not in kwargs else str(kwargs['title']),
		'save_as': None if 'save_as' not in kwargs else str(kwargs['save_as'])
	}

	fig, ax = plt.subplots(figsize=opts['figsize'])
	ax.hist(x, bins='auto')  # returns np.ndarray: n, bins, patches

	if opts['best_fit']:
		# TODO: figure out how to plot a best fit line for a histogram
		pass

	ax.set_xlabel(str(opts['x_label']), fontsize=12)
	ax.set_ylabel(str(opts['y_label']), fontsize=12)
	ax.set_title(str(opts['title']), fontsize=15)
	plt.figtext(x=0.79, y=0.05, s='Data: nflfastR.', fontsize=10)

	return fig, ax


# basic way to build scatterplot
def build_scatterplot(x: pd.Series, y: pd.Series, **kwargs) -> (plt.Figure, plt.Axes):
	"""
	function to build a scatter plot for the varibles x and y.
	code entirely adapted from Deryck97's amazing tutorial on nflfastR
	for python
	:param x: variable that will be plotted on the X-axis
	:param y: variable that will be plotted on the y-axis
	:param kwargs: keyword arguments
	Args:
		figsize (tuple(int, int)): specify the size of the plot. defaults to (15, 15)
		best_fit (bool): if True, will plot a best-fit curve on the histogram. Defaults to False
		gridlines (bool): if True, will add a grid to the plot. Defaults to True.
		x_label (str): the title written to the x-axis. Defaults to 'X'
		y_label (str): the title written to the y-axis. Defaults to 'y'
		title (str): the title of the graph or plot. Defaults to 'title'
		save_as (str): the filename to which the function will attempt to save the generated plot. If None (default),
		no save will occur
	:return: tuple of (plt.Figure, plt.Axes) objects. This allows for additional customization to the plot and provides
	flexibility in the library
	"""
	# validate input series
	if x.size <= 0 or y.size <= 0:
		raise ValueError("Invalid arguments passed to function (build-scatterplot): size of input series is 0.")

	opts = {
		'figsize': (15, 15) if 'figsize' not in kwargs else kwargs['figsize'],
		'best_fit': True if 'best_fit' not in kwargs else kwargs['best_fit'],
		'gridlines': True if 'gridlines' not in kwargs else kwargs['gridlines'],
		'x_label': 'X' if 'x_label' not in kwargs else str(kwargs['x_label']),
		'y_label': 'y' if 'y_label' not in kwargs else str(kwargs['y_label']),
		'title': 'Title' if 'title' not in kwargs else str(kwargs['title']),
		'save_as': None if 'save_as' not in kwargs else str(kwargs['save_as'])
	}

	fig, ax = plt.subplots(figsize=opts['figsize'])

	ax.scatter(x, y, s=0.001, color='navy')
	if opts['best_fit']:
		ax.plot(
			np.unique(x),
			np.poly1d(np.polyfit(x, y, 1)) * np.unique(x)
		)

	if opts['gridlines']:
		ax.grid(zorder=0, alpha=0.4)
		ax.set_axisbelow(True)

	ax.set_xlabel(str(opts['x_label']), fontsize=12)
	ax.set_ylabel(str(opts['y_label']), fontsize=12)
	ax.set_title(str(opts['title']), fontsize=15)

	plt.figtext(x=0.79, y=0.05, s='Data: nflfastR.', fontsize=10)

	if opts['save_as'] is not None:
		plt.savefig(opts['save_as'], dpi=400)

	return fig, ax


def build_logoplot(x: pd.Series, y: pd.Series, **kwargs) -> (plt.Figure, plt.Axes):
	"""
	Function that builds a scatterplot using team logos instead of the default markers used
	by matplotlib
	:param x: variable that will be plotted on the X-axis
	:param y: variable that will be plotted on the y-axis
	:param kwargs: keyword arguments
	Args:
		figsize (tuple(int, int)): specify the size of the plot. defaults to (15, 15)
		best_fit (bool): if True, will plot a best-fit curve on the histogram. Defaults to False
		gridlines (bool): if True, will add a grid to the plot. Defaults to True.
		x_label (str): the title written to the x-axis. Defaults to 'X'
		y_label (str): the title written to the y-axis. Defaults to 'y'
		title (str): the title of the graph or plot. Defaults to 'title'
		save_as (str): the filename to which the function will attempt to save the generated plot. If None (default),
		no save will occur
	:return: tuple of (plt.Figure, plt.Axes) objects. This allows for additional customization to the plot and provides
	flexibility in the library
	"""
	# validate input series
	if x.size <= 0 or y.size <= 0:
		raise ValueError("Invalid arguments passed to function (build-scatterplot): size of input series is 0.")

	opts = {
		'figsize': (15, 15) if 'figsize' not in kwargs else kwargs['figsize'],
		'best_fit': True if 'best_fit' not in kwargs else kwargs['best_fit'],
		'gridlines': True if 'gridlines' not in kwargs else kwargs['gridlines'],
		'x_label': 'X' if 'x_label' not in kwargs else str(kwargs['x_label']),
		'y_label': 'y' if 'y_label' not in kwargs else str(kwargs['y_label']),
		'title': 'Title' if 'title' not in kwargs else str(kwargs['title']),
		'save_as': None if 'save_as' not in kwargs else str(kwargs['save_as'])
	}

	fig, ax = plt.subplots(figsize=opts['figsize'])

	ax.scatter(x, y, s=0.001)

	# add logos
	logo_paths = __get_logos()
	for _x, _y, path in zip(x, y, logo_paths):
		ab = AnnotationBbox(
			__get_image(path),
			(_x, _y),
			frameon=False,
			fontsize=5
		)
		ax.add_artist(ab)

	# add grid
	ax.grid(zorder=0, alpha=0.4)
	ax.set_axisbelow(True)

	# add labels and text
	ax.set_xlabel(opts['x_label'], fontsize=16)
	ax.set_ylabel(opts['y_label'], fontsize=16)
	ax.set_title(opts['title'], fontsize=22)
	plt.figtext(0.81, 0.07, 'Data: nflfastR', fontsize=12)

	if opts['save_as'] is not None:
		plt.savefig(opts['save_as'], dpi=400)

	return fig, ax


def build_hbar(x: pd.Series, **kwargs) -> None:
	"""
	:param x:
	:param y:
	:return:
	"""
	if x.size <= 0:
		raise ValueError("Invalid arguments passed to function (build-scatterplot): size of input series is 0.")

	opts = {
		'figsize': (15, 15) if 'figsize' not in kwargs else kwargs['figsize'],
		'x_label': 'X' if 'x_label' not in kwargs else str(kwargs['x_label']),
		'y_label': 'y' if 'y_label' not in kwargs else str(kwargs['y_label']),
		'title': 'Title' if 'title' not in kwargs else str(kwargs['title']),
		'save_as': None if 'save_as' not in kwargs else str(kwargs['save_as'])
	}

	raise NotImplementedError("This function is not supported by this version of pylon. ")


def build_vbar(x: pd.Series, **kwargs) -> (plt.Figure, plt.Axes):
	"""
	Plots a vertical bar chart for a set of data points.
	:param x: set of input datapoints
	:param kwargs: keyword arguments
	Args:
		figsize (tuple(int, int)): specify the size of the plot. defaults to (15, 15)
		avg_line (bool): if True, will add a line demarcating the level of the average value of x
		avg_text (str): The label given to the average line, if one exists. Defaults to 'NFL average'. Must have
		avg_line = True for this to be active, otherwise function throws exception
		logos (bool): if True, adds logos to the top of the bars (good if each data point represents a team).
			Defaults to True.
		x_label (str): the title written to the x-axis. Defaults to 'X'
		y_label (str): the title written to the y-axis. Defaults to 'y'
		title (str): the title of the graph or plot. Defaults to 'title'
		save_as (str): the filename to which the function will attempt to save the generated plot. If None (default),
			no save will occur
	:return: tuple of (plt.Figure, plt.Axes) objects. This allows for additional customization to the plot and provides
	flexibility in the library
	"""
	# validate input series
	if x.size <= 0:
		raise ValueError("Invalid arguments passed to function (build-vbar): size of input series is 0.")

	opts = {
		'figsize': (30, 10) if 'figsize' not in kwargs else kwargs['figsize'],
		'avg_line': True if 'avg_line' not in kwargs else kwargs['avg_line'],
		'avg_text': 'NFL Average' if 'avg_text' not in kwargs else kwargs['avg_text'],
		'logos': True if 'logos' not in kwargs else kwargs['logos'],
		'x_label': 'X' if 'x_label' not in kwargs else str(kwargs['x_label']),
		'y_label': 'y' if 'y_label' not in kwargs else str(kwargs['y_label']),
		'title': 'Title' if 'title' not in kwargs else str(kwargs['title']),
		'save_as': None if 'save_as' not in kwargs else str(kwargs['save_as'])
	}

	fig, ax = plt.subplots(figsize=opts['figsize'])

	if opts['avg_line']:
		ax.axhline(y=x.mean(), linestyle='--', color='black')

	if opts['logos']:
		logo_paths = __get_logos()
		for _x, _y, path in zip(np.arange(x.size), x.mean() + 0.005, logo_paths):
			ab = AnnotationBbox(
				__get_image(path),
				(_x, _y),
				frameon=False,
				fontsize=5
			)
			ax.add_artist(ab)

	ax.bar(np.arange(x.size), x, color=TEAM_COLORS.values(), width=0.6)

	# add grid across the y-axis
	ax.grid(zorder=0, alpha=0.07, axis='y')
	ax.set_axisbelow(True)
	ax.set_xticks(np.arange(x.size))

	# add labels
	ax.set_xlabel(opts['x_label'], fontsize=16)
	ax.set_ylabel(opts['y_label'], fontsize=16)
	ax.set_title(opts['title'], fontsize=22)
	plt.figtext(0.81, 0.07, 'Data: nflfastR', fontsize=12)

	if opts['avg_text']:
		if not opts['avg_line']:
			raise ValueError("Invalid arguments to function (build-vbar). Cannot specify avg_text if avg_line is False.")
		plt.text(x.size - 1, x.mean() + 0.005, opts['avg_text'], fontsize=12)

	if opts['save_as'] is not None:
		plt.savefig(opts['save_as'], dpi=400)

	return fig, ax
