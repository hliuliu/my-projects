
import stats,unittest


def makedata(data,expected_mean=None,expected_median=None):
	return data, dict(
		mean=expected_mean,
		median=expected_median
		)



class test_stats_module(unittest.TestCase):
	def setUp(self):
		self.nice_samples=[
		makedata([0],expected_mean=0,expected_median=0),
		makedata([1,1],expected_mean=1,expected_median=1),
		makedata([1,2,3],expected_mean=2,expected_median=2),
		makedata([1,3,5,9],expected_mean=4.5,expected_median=4),
		makedata([2,2,5],expected_mean=3,expected_median=2),
		makedata([4,10,7],expected_mean=7,expected_median=7),
		makedata([9,8,2,6,20],expected_mean=9,expected_median=8),
		]

	def test_mean(self):
		for data,summary in self.nice_samples:
			self.assertEquals(summary['mean'],stats.mean(*data))

	def test_median(self):
		for data,summary in self.nice_samples:
			self.assertEquals(summary['median'],stats.median(*data))


if __name__=='__main__':
	unittest.main()



