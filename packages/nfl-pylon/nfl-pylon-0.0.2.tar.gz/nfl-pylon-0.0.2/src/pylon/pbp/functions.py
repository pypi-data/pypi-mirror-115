# python 3.6
# wrappers around nflfastR functions
# that return pandas DataFrames
import pandas as pd
from ..util.urls import PBP_URL


def build_nflfastr_pbp(game_ids: list, decode: bool = True, rules: bool = True) -> pd.DataFrame:
	raise NotImplementedError("This function is not supported by this version of pylon.")


def load_pbp(
		seasons: list, only_regular_season: bool = False, remove_plays=True
) -> pd.DataFrame:
	"""
	Loads a cleaned play-by-play dataset obtained from the nflfastR data
	repository for all the season in seasons. Inspired by Deryck97's nflfastR python guide.
	:param seasons: list of seasons to scrape data from
	:param only_regular_season: if True, filters out non-regular season (i.e. pre and postseason) plays
	from the dataframe
	:param remove_plays: if True, removes plays that are typically unused in analysis such as field goals
	and kickoffs and kneel downs
	:return: pandas.DataFrame object representing a dataset of plays
	"""
	pbp_dfs = [
		pd.read_csv(
			PBP_URL.format(season=season),
			compression='gzip',
			error_bad_lines=False,
			low_memory=False  # this disables a warning that pandas gives for some reason. warning isn't important.
		)
		for season in seasons
		if 1999 <= int(season) <= 2020
	]

	df = pd.concat(pbp_dfs).reset_index(drop=True).copy(deep=True)

	# cleaning code adapted directly from Deryck97's nflfastR python guide.
	# https://gist.github.com/Deryck97/dff8d33e9f841568201a2a0d5519ac5e
	if only_regular_season:
		df = df.loc[df.season_type == 'REG'].copy()

	# we want to remove plays like kickoffs, field goals, kneel downs, etc.
	# since they usually don't have any effect on the analysis
	if remove_plays:
		df = df.copy(deep=True).loc[
			(df.play_type.isin(['no_play', 'pass', 'run']) & (~df.epa.isna()))
		]

	# change play type to match play call. for example,
	# sometimes QB scrambles get mistakenly labeled as run
	# plays but we want to analyze them as pass plays
	# throws a SettingWithCopyWarning that I can't figure out how to get rid of
	df.play_type.loc[df['pass'] == 1] = 'pass'
	df.play_type.loc[df.rush == 1] = 'run'

	# just for good measure.
	df.reset_index(drop=True)

	return df
