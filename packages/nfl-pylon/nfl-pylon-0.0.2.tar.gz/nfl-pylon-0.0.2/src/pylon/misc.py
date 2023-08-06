# python 3.6
# file for the nflfastR functions I couldn't find a place for
import pandas as pd
import pyreadr

from src.pylon.util.urls import ROSTER_URL, STATS_URL


# TODO: look into the Sleeper API to get roster data. For now,
# 		we just use the repo that has the data already stored
def get_roster(seasons: list) -> pd.DataFrame:
	"""
	Obtain rosters for all NFL teams across the given seasons
	:param seasons: list of integers representing seasons where each season[i] in the range [1999, 2020]
	:return: pandas DataFrame object
	"""
	roster_dfs = [
		pd.read_csv(ROSTER_URL.format(season=season), error_bad_lines=False)
		for season in seasons
		if 1999 <= int(season) <= 2020
	]

	for roster in roster_dfs:
		print(roster)

	df = pd.concat(roster_dfs).reset_index(drop=True)
	return df


def get_schedules(seasons: list, filepath: str = '../data/schedules/sched_{season}.rds') -> pd.DataFrame:
	"""
	Function that obtains a dataframe containing the scheduling data for the specified seasons by scraping a local
	object file
	:param seasons: the list of seasons to scrape for schedule data
	:param filepath: the location of the object file containing the schedule data on disk. Not recommended to
	change the default
	:return: dataframe containing schedule data.
	"""
	# https://stackoverflow.com/questions/64178038/how-to-read-a-rds-file-from-a-url-in-python
	# credit to ofajardo for developing the pyreadr package
	schedule_dfs = [
		pyreadr.read_r(filepath.format(season=season))[None]
		for season in seasons
		if 1999 <= int(season) <= 2020
	]

	df = pd.concat(schedule_dfs).reset_index(drop=True)
	return df


def get_stats(serialize: bool = False) -> pd.DataFrame:
	"""
	function that obtains player statistics
	:param serialize: if this is True, use serialization for greater efficiency (not supported yet)
	:return: pandas DataFrame object with all NFL player stats as maintained by nflfastR.
	"""
	df = pd.read_csv(STATS_URL, compression='gzip', low_memory=False)
	return df
