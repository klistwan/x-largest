import argparse
import heapq
import sys

class Record:
	def __init__(self, file_line):
		uid, value = file_line.strip().split()
		self.uid = uid
		self.value = int(value)

	def __lt__(self, other):
	    return self.value < other.value


class TopRecordHandler:
	def __init__(self, x: int):
		self.heap = []
		self.max_elements = x

	def add(self, record: Record) -> None:
		if len(self.heap) < self.max_elements:
			self.heap.append(record)
			if len(self.heap) == self.max_elements:
				heapq.heapify(self.heap)
		else:
			if self.heap[0] < record:
				heapq.heapreplace(self.heap, record)

	def output(self):
		print("\n".join([r.uid for r in self.heap]))


def main():
	parser = argparse.ArgumentParser(description='Report x largest values.')
	parser.add_argument('x_largest', type=int, help='number of largest values')
	parser.add_argument('--file', '-f', nargs='?', help='absolute path to an input file')
	_args = parser.parse_args()

	# Open from file if supplied, else from stdin.
	lines = open(_args.file) if _args.file else sys.stdin

	handler = TopRecordHandler(_args.x_largest)
	for line in lines:
		record = Record(line)
		handler.add(record)
	handler.output()


if __name__ == '__main__':
	main()
