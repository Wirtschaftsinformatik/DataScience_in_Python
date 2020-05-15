############################################################
# Damian Jordanov - FSU Jena - Python Workshop - SoSe 2020 #
############################################################

from functools import reduce

import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib import colors

DATA_URL = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
OUTBREAK_THRESHOLD = 200
REGIONS = ['Italy', 'France', 'Germany', 'Spain', 'China', 'South_Korea', 'United_Kingdom', 'Australia', 'United_States_of_America', 'Vietnam']
WINDOW_MOVSUM = 28
WINDOW_MOVAV = 7

def df_clean(df):

	# create datetime column,
	daymonthyear = df[['day', 'month', 'year']]
	df['date'] = pd.to_datetime(daymonthyear)

	# drop superflous columns
	df = df.drop(['dateRep', 'day', 'month', 'year', 'countryterritoryCode', 'continentExp'], axis=1)

	# sort by countriesAndTerritories + date and set countriesAndTerritories as index
	df = df.sort_values(['countriesAndTerritories', 'date'], ascending=[True, True])
	df.set_index(keys = ['countriesAndTerritories'], drop = False, inplace = True)
	df.index.name = None

	# rename ambiguous columns
	df = df.rename(columns={'cases': 'nccases', 'deaths': 'ndeaths'}) # nccases: new confirmed cases, ndeaths: new deaths

	return df


def df_calc_secondary(df):

	df_grouped_region = df.groupby('countriesAndTerritories')

	# cumulated sums and log of cumulated sums
	df['cccases'] = df_grouped_region['nccases'].cumsum()
	df['cccases_log'] = np.log(df['cccases'], where = df['cccases'] > 0)

	df['cdeaths'] = df_grouped_region['ndeaths'].cumsum()
	df['cdeaths_log'] = np.log(df['cdeaths'], where = df['cdeaths'] > 0)

	# rolling rolling sum
	df['nccases_movsum'] = df_grouped_region['nccases'].rolling(WINDOW_MOVSUM).sum().values
	df['nccases_movsum_movav'] = df_grouped_region['nccases_movsum'].rolling(WINDOW_MOVAV, center = True).mean().values

	df['ndeaths_movsum'] = df_grouped_region['ndeaths'].rolling(WINDOW_MOVSUM).sum().values
	df['ndeaths_movsum_movav'] = df_grouped_region['ndeaths_movsum'].rolling(WINDOW_MOVAV, center = True).mean().values

	# growth rates
	df['nccases_movsum_movav_chng'] = df_grouped_region['nccases_movsum_movav'].pct_change()

	# death rate from movsum
	df['death_rate'] = df['ndeaths_movsum_movav'] / df['nccases_movsum_movav']

	return df

def df_calc_days_since_outbreak(df):

	# get all rows after outbreak
	df_over_threshold = df.loc[df['cccases'] >= OUTBREAK_THRESHOLD]

	# filter to first rows (per region) after outbreak
	threshold_rows = df_over_threshold.groupby(df_over_threshold.countriesAndTerritories).head(1)

	# initialize days_since_outbreak as date of outbreak in that region
	for region in threshold_rows.index:
		df.loc[region, 'days_since_outbreak'] = threshold_rows.loc[region, 'date']

	# compute days since outbreak
	df['days_since_outbreak'] = (df['date'] - df['days_since_outbreak']).apply(lambda x: x.days)

	return df


def df_cut_before_outbreak(df):
	return df.loc[df['days_since_outbreak'] >= 0]

def vis_cmovsum2growth_drate_curr(regions):

	# Initialize plot with last received data ...
	dfr = df.loc[REGIONS]
	dfr = dfr.dropna()
	dfr_grouped = dfr.dropna().groupby('countriesAndTerritories')
	dfrs = dfr_grouped.tail(1)

	# create basic plot with initial datapoints
	plt.clf()
	fig, ax = plt.subplots()

	cmap = cm.get_cmap('gist_heat_r', 1000)
	linthresh = 0.25
	norm = colors.SymLogNorm(linthresh = linthresh, vmin = 0, vmax = 1, base = np.e)

	scatter = ax.scatter(dfrs['nccases_movsum_movav'], dfrs['nccases_movsum_movav_chng'], s = 750, label = dfrs.index, c = dfrs['death_rate'], alpha = 0.8, cmap = cmap, norm = norm, edgecolors = 'black')

	# set zoom and scale
	ax.set_xscale('log')

	# color legend
	linticks = np.linspace(0, linthresh, 5)
	logticks = np.logspace(np.log10(linthresh), 0, 5)
	ticks = np.concatenate((linticks, logticks), axis = 0)
	colorbar = fig.colorbar(scatter, cmap = cmap, norm = norm, ticks = ticks, label = 'Death Rate')
	colorbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))

	# descriptions
	ax.set_title('Covid-19 Confirmed Cases to Growth Rate with Death Rate')
	ax.set_xlabel('Confirmed Cases in the last ' + str(WINDOW_MOVSUM) + ' Days')
	ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
	ax.set_ylabel('Growth Rate')

	# annotations
	annotations = {}
	for idx, geoId in np.ndenumerate(dfrs['geoId'].values):
		i = idx[0]
		annotations[geoId] = ax.annotate(geoId, xy = (dfrs['nccases_movsum_movav'][i], dfrs['nccases_movsum_movav_chng'][i]), ha='center', va='center', color = 'blue', fontweight = 'bold')

	# save created plot
	plt.savefig('vis_cmovsum2growth_drate_curr.png')

def vis_cmovsum2growth_drate_timelapse(regions):

	# Initialize plot with data from day of outbreak
	dfr = df.loc[regions]
	dfr = dfr.dropna()
	dfrs = dfr.loc[dfr['days_since_outbreak'] == 0]

	# create basic plot with initial datapoints
	plt.clf()
	fig, ax = plt.subplots()
	cmap = cm.get_cmap('gist_heat_r', 1000)
	linthresh = 0.25
	norm = colors.SymLogNorm(linthresh = linthresh, vmin = 0, vmax = 1, base = np.e)

	scatter = ax.scatter(dfrs['nccases_movsum_movav'], dfrs['nccases_movsum_movav_chng'], s = 750, label = dfrs.index, c = dfrs['death_rate'], alpha = 0.8, cmap = cmap, edgecolors = 'black', norm = norm)

	# set zoom and scale
	ax.set_ylim(-0.3, 0.8)
	ax.set_xscale('log')
	ax.set_xlim(right = 10000000)

	# color legend
	linticks = np.linspace(0, linthresh, 5)
	logticks = np.logspace(np.log10(linthresh), 0, 5)
	ticks = np.concatenate((linticks, logticks), axis = 0)
	colorbar = fig.colorbar(scatter, cmap = cmap, norm = norm, label = 'Death Rate', ticks = ticks)
	colorbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))

	# descriptions
	ax.set_title('Covid-19 Confirmed Cases to Growth Rate on Day 0 after Outbreak')
	ax.set_xlabel('Confirmed Cases in the last ' + str(WINDOW_MOVSUM) + ' Days')
	ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
	ax.set_ylabel('Growth Rate')

	# initialize annotations
	annotations = {}
	for idx, geoId in np.ndenumerate(dfrs['geoId'].values):
		i = idx[0]
		annotations[geoId] = ax.annotate(geoId, xy = (dfrs['nccases_movsum_movav'][i], dfrs['nccases_movsum_movav_chng'][i]), ha='center', va='center', color = 'blue', fontweight = 'bold')

	def update(day):

		# update plot with data from given day ...

		dfrs = dfr.loc[dfr['days_since_outbreak'] == day]

		scatter.set_offsets(np.c_[ dfrs['nccases_movsum_movav'], dfrs['nccases_movsum_movav_chng'] ])
		scatter.set_color( c = dfrs['death_rate'].apply(lambda x: cmap(x)) )
		scatter.set_edgecolors('black')

		# update position of point labels
		geoIds = dfrs['geoId'].values
		delkeys = []
		for key, ann in annotations.items():
			if np.in1d(key, geoIds):
				ann.set_x(dfrs.loc[ dfrs.geoId == key ]['nccases_movsum_movav'])
				ann.set_y(dfrs.loc[ dfrs.geoId == key ]['nccases_movsum_movav_chng'])
			else:
				delkeys.append(key)

		# create annotations of new data points (in case a day is missing in the reported data)
		for geoId in geoIds:
			if not geoId in [k for k in annotations]:
				annotations[geoId] = ax.annotate(geoId, xy = (dfrs.loc[ dfrs.geoId == geoId ]['nccases_movsum_movav'], dfrs.loc[ dfrs.geoId == geoId ]['nccases_movsum_movav_chng']), ha='center', va='center', color = 'blue', fontweight = 'bold')

		# delete annotations of no-longer-present points
		for key in delkeys:
			annotations[key].remove()
			del annotations[key]

		# update title
		ax.set_title('Covid-19 Confirmed Cases to Growth Rate on Day ' + str(day) + ' after Outbreak')

		return scatter

	max_days = int(dfr['days_since_outbreak'].max() - 1)
	anim = animation.FuncAnimation(fig, update, frames = max_days, interval = 500)

	# save created animation
	writer = animation.PillowWriter()
	anim.save('vis_cmovsum2growth_drate_timelapse.gif', writer = writer)


def vis_turning_point(regions):

	# Visualize the point at which the number of new confirmed cases per day no longer grows as days_since_outbreak to cumulated confirmed cases ...
	dfr = df.loc[REGIONS]
	after_turning_point = dfr.loc[dfr['nccases_movsum_movav_chng'] <= 0]
	turning_point = after_turning_point.groupby(after_turning_point['countriesAndTerritories']).first()

	# built plot with days_since_outbreak - cccases
	# (with population as size and death rate as color, because why not)

	plt.clf()
	fig, ax = plt.subplots()
	cmap = cm.get_cmap('gist_heat_r', 1000)
	linthresh = turning_point['death_rate'].median()
	norm = colors.SymLogNorm(linthresh = linthresh, vmin = turning_point['death_rate'].min(), vmax = turning_point['death_rate'].max(), base = np.e)
	scatter = ax.scatter(turning_point['days_since_outbreak'], turning_point['cccases'], s = 0.5 * np.sqrt(turning_point['popData2018']), label = turning_point.index, alpha = 0.8, cmap = cmap, c = turning_point['death_rate'], edgecolors = 'black')

	# color legend
	colorbar = fig.colorbar(scatter, cmap = cmap, norm = norm, label = 'Death Rate')
	colorbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))

	# set zoom and scale
	ax.set_yscale('log')

	# descriptions
	ax.set_title('Turning Point after Initial Outbreak')
	ax.set_xlabel('Days since '  +str(OUTBREAK_THRESHOLD) + ' Cumulated Confirmed Cases')
	ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
	ax.set_ylabel('Cumulated Confirmed Cases at Turning Point')

	# initialize annotations
	annotations = {}
	for idx, geoId in np.ndenumerate(turning_point['geoId'].values):
		i = idx[0]
		annotations[geoId] = ax.annotate(geoId, xy = (turning_point['days_since_outbreak'][i], turning_point['cccases'][i]), ha='center', va='center', color = 'blue', fontweight = 'bold')

	# save created plot
	plt.savefig('vis_turning_point.png', bbox_inches = "tight")

def vis_region_dendrogram():

	def build_regcol_df(df, col, min_observations):
		regcol_df = pd.DataFrame()
		for region in df.index:
			observations = pd.Series(dfnna.loc[region, col]).reset_index(drop = True)
			if (observations.size >= min_observations):
				regcol_df[region] = observations

		return regcol_df

	def rsme(a, b):
		size = min(a.size, b.size)
		a = a[0:size]
		b = b[0:size]
		return mean_squared_error(a, b)

	def norm_df(df):
		min = df.min().min()
		max = df.max().max()
		return pd.DataFrame( [ (x - min) / (max - min) for x in df.values] , df.index)

	# the script will create one comparison matrix per column to be compared
	dfnna = df.dropna()
	cluster_cols = ['cccases_log', 'cdeaths_log', 'death_rate']

	# build dataframe with only the given columns values and one column per region
	regcol_dfs = [build_regcol_df(dfnna, col, 30) for col in cluster_cols]

	# build distance dataframes as rsme from the previously built dataframes
	dist_dfs = [df.corr(rsme) for df in regcol_dfs]
	for dist_df in dist_dfs:
		np.fill_diagonal(dist_df.values, 0)

		# normalize distance dataframes
	norm_dist_dfs = [norm_df(dist_df) for dist_df in dist_dfs]

	# turn distance matrizes into a single distance matrix to be used for clustering
	norm_dist_df = reduce(lambda a, b: a + b, norm_dist_dfs) / len(norm_dist_dfs)

	# do clustering
	dist_condens = distance.squareform(norm_dist_df)
	link = linkage(dist_condens, method = 'centroid', optimal_ordering = True)

	# visualize clustering as dendrogram
	plt.clf()
	dendro = dendrogram(link, labels = dist_df.index, leaf_rotation = 90, leaf_font_size = 4)

	# save dendrogram
	plt.savefig('vis_region_dendrogram.pdf')

df = pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
df = df_clean(df)
df = df_calc_secondary(df)
df = df_calc_days_since_outbreak(df)
df = df_cut_before_outbreak(df)

vis_cmovsum2growth_drate_curr(REGIONS)
vis_cmovsum2growth_drate_timelapse(REGIONS)
vis_turning_point(REGIONS)
vis_region_dendrogram()