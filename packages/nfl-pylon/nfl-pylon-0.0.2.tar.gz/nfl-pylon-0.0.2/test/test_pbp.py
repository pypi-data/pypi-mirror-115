import unittest

from src.pylon.pbp import functions


class TestPBP(unittest.TestCase):
	def test_load(self):
		pbp = functions.load_pbp([2019])

		# testing a successful load
		actual_shape = pbp.shape
		expected_shape = (38151, 372)
		self.assertEqual(actual_shape, expected_shape)

		# assert that we don't only have the regular season
		df = pbp.loc[pbp.season_type == 'REG'].copy()
		self.assertNotEqual(df.shape, pbp.shape)

	def test_load_multiple(self):
		pbp = functions.load_pbp(
			[2016, 2017, 2018, 2019]
		)

		# test success
		actual_shape = pbp.shape
		expected_shape = (152450, 372)
		self.assertEqual(actual_shape, expected_shape)


if __name__ == '__main__':
	unittest.main()
