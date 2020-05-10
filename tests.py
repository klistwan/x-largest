import unittest

from main import Record


class TestRecord(unittest.TestCase):

	def test_instantiation(self):
		record = Record("1426828028 350")
		assert record.uid == "1426828028"
		assert record.value == 350


	def test_less_than(self):
		record_a = Record("10 350")
		record_b = Record("5 351")
		assert record_a < record_b




if __name__ == "__main__":
	unittest.main()