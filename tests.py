import contextlib
import io
import sys
import unittest

from unittest.mock import patch


from main import Record, TopRecordHandler, main, parse_args


class TestRecord(unittest.TestCase):

	def test_instantiation(self):
		record = Record("1426828028 350")
		self.assertEqual(record.uid, "1426828028")
		self.assertEqual(record.value, 350)


	def test_less_than(self):
		record_a = Record("10 350")
		record_b = Record("5 351")
		self.assertTrue(record_a < record_b)


class TestTopRecordHandler(unittest.TestCase):

	def test_instantiation(self):
		tpr = TopRecordHandler(1)
		self.assertFalse(tpr.heap)
		self.assertEqual(tpr.max_elements, 1)

	def test_add_record(self):
		tpr = TopRecordHandler(1)
		sample_record = Record("10 350")
		tpr.add(sample_record)
		self.assertEqual(len(tpr.heap), 1)
		self.assertEqual(tpr.heap[0], sample_record)

	def test_heapify_when_max_heap_size_reached(self):
		tpr = TopRecordHandler(3)
		large, small, mid = [Record(data) for data in ["1 10", "5 5", "9 8"]]
		for record in [large, small, mid]:
			tpr.add(record)
		self.assertEqual(tpr.heap[0], small)

	def test_heap_does_not_exceed_max_element_size(self):
		tpr = TopRecordHandler(1)
		tpr.add(Record("1 1"))
		tpr.add(Record("2 2"))
		self.assertEqual(len(tpr.heap), tpr.max_elements)

	def test_new_large_value_replaces_existing(self):
		tpr = TopRecordHandler(1)
		small, large = Record("1 1"), Record("2 2")
		for record in [small, large]:
			tpr.add(record)
		self.assertEqual(tpr.heap[0], large)


class TestParser(unittest.TestCase):
	def test_single_argument(self):
		parser = parse_args(['5'])
		self.assertEqual(parser.x_largest, 5)
		self.assertEqual(parser.file, None)

	def test_both_arguments(self):
		parser = parse_args(['5', '--file', 'test.txt'])
		self.assertEqual(parser.x_largest, 5)
		self.assertEqual(parser.file, 'test.txt')


class TestMain(unittest.TestCase):
	def setUp(self):
		self.stdout = io.StringIO()

	def test_main_with_stdin(self):
		input_file = open('sample_data/a.input')
		output_file = open('sample_data/a.output')

		with patch.object(sys, 'argv', ['main.py', '3']), \
			patch.object(sys, 'stdin', input_file), \
			contextlib.redirect_stdout(self.stdout):
			main()
			self.assertEqual(self.stdout.getvalue(), output_file.read())

		input_file.close()
		output_file.close()

	def test_main_with_file_arg(self):
		output_file = open('sample_data/b.output')

		with patch.object(sys, 'argv', ['main.py', '2', '-f', 'sample_data/b.input']), \
			contextlib.redirect_stdout(self.stdout):
			main()
			self.assertEqual(self.stdout.getvalue(), output_file.read())

		output_file.close()


if __name__ == "__main__":
	unittest.main()
