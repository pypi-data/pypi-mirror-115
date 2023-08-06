# python 3.6
# all the nflfastR calculation functions go here
import pandas as pd
import pyreadr

from src.pylon.util.urls import STATS_URL

# TODO: use the nflfastR rda model objects for now. maybe we want to build our own models?
# 		for now, put the rda files in data/models/ and read from there.


def ep(pbp: pd.DataFrame) -> pd.DataFrame:
	# rda = pyreadr.read_r('../data/models/ep_model.rda')
	# model = rda[rda.keys()[0]]
	raise NotImplementedError("This function is not currently supported by this version of pylon.")


def wp(pbp: pd.DataFrame) -> pd.DataFrame:
	# rda = pyreadr.read_r('../data/models/wp_model.rda')
	# model = rda[rda.keys()[0]]
	raise NotImplementedError("This function is not currently supported by this version of pylon.")


def player_stats(pbp: pd.DataFrame, weekly: bool = False) -> pd.DataFrame:
	raise NotImplementedError("This function is not currently supported by this version of pylon.")
	# df = pd.read_csv(STATS_URL, compression='gzip', low_memory=True)
	# return df
