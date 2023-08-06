# python 3.6
# basic data analysis functions
import pandas as pd
from copy import deepcopy


def find_game(pbp: pd.DataFrame, **kwargs: dict) -> pd.DataFrame:
	"""
	function wrapper around finding a specific game in a season-wide play-by-play
	dataset
	:param pbp: season worth of play-by-play data
	:param kwargs: the keys used to query for a particular game. can either be
	- home_team: HOME team abbreviation
	- away_team: AWAY team abbreviation
	OR
	- game_id: NFL gamecenter ID
	but NOT both
	:return: filtered dataframe with play-by-play data for the queried game
	"""
	df = pbp.copy(deep=True)

	if {"game_id", "home_team", "away_team"} is set(kwargs.keys()):
		raise ValueError("Cannot specify both game_id AND home, away team")

	if "home_team" in kwargs and "away_team" in kwargs:
		home = kwargs["home_team"]
		away = kwargs["away_team"]
		df = df.loc[(df.home_team == home) & (df.away_team == away)]
	else:
		game_id = kwargs["game_id"]
		df = df.loc[df.game_id == game_id]
	return df


def get_performance(pbp: pd.DataFrame, pos: str, **kwargs) -> pd.DataFrame:
	"""
	function that returns season-wide statistics for players at a particular position
	can specify metrics in kwargs
	:param pbp: play-by-play dataset
	:param pos: position to query for. must be one of
	- QB
	- RB
	- WR
	- TE
	:param kwargs: additional parameters can be included in the query. currently only supports EPA.
	- 	agg: aggregation data you can pass to the function
	- 	min_plays: minimum number of plays for inclusion into analysis. default is 200.
	- 	sort: will sort the dataframe before returning. default is true.
	- 	sort_direction: must only be present if sort is present.
		Set this to true if you want to sort in ascending order, false otherwise. default is false.
	- 	sort_by: must only be present if sort is present. column on which to sort each record. default is EPA
	- 	round: precision to which dataframe will round values. default is 3.
	:return: filtered and sorted dataframe containing results of player performance
	"""
	# TODO: write a subroutine to validate kwargs
	ops = {
		'epa': 'mean',
		'play_id': 'count'
	}
	if 'agg' in kwargs:
		ops = deepcopy(kwargs['agg'])

	category_map = {
		"QB": "passer",
		"RB": "rusher",
		"WR": "receiver",  # verify that these are accurate
		"TE": "receiver"
	}
	if pos not in category_map:
		raise ValueError(f"Cannot get performance for the position {pos}.")
	player_type = category_map[pos]

	if player_type == 'passer':
		ops['cpoe'] = 'mean'

	players = pbp.groupby(
		[player_type, 'posteam'],
		as_index=False
	).agg(ops)

	# we want to establish a certain threshold
	# so that we only include meaningful data in the
	# analysis.
	if 'min_plays' in kwargs:
		mp = kwargs['min_plays']
	else:
		if player_type == 'passer':
			mp = 200
		elif player_type == 'rusher':
			mp = 100
		else:
			mp = 30
	players = players.copy().loc[players.play_id >= mp]

	# have to configure the sorting options so its invalid to specify sort properties
	# without first specifying that they want to sort.
	if 'sort' not in kwargs and ('sort_descending' in kwargs or 'sort_by' in kwargs):
		raise ValueError("Error! Trying to specify sorting behavior without specifying sort.")
	sort_options = {
		'sort': True if 'sort' not in kwargs else kwargs['sort'],
		'sort_ascending': False if 'sort_dir' not in kwargs else kwargs['sort_dir'],
		'sort_by': 'epa' if 'sort_by' not in kwargs else kwargs['sort_by']
	}
	if sort_options['sort']:
		players.sort_values(sort_options['sort_by'], ascending=sort_options['sort_ascending'], inplace=True)

	# 3 just seems like a good number. Deryck97 used 2, but I like 3 better as a number.
	precision = 3 if 'round' not in kwargs else kwargs['round']
	players = players.round(precision)

	return players
