import argparse
import heapq
import sys
import typing

class Record:
	def __init__(self, file_line):
		uid, value = file_line.strip().split()
		self.uid = uid
		self.value = int(value)

	def __lt__(self, other):
	    return self.value < other.value


class TopRecordHandler:
	def __init__(self, x: int) -> None:
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

	def output(self) -> None:
		print("\n".join([r.uid for r in self.heap]))


def parse_args(args: typing.List[str]):
	parser = argparse.ArgumentParser(description='Report x largest values.')
	parser.add_argument('x_largest', type=int, help='number of largest values')
	parser.add_argument('--file', '-f', nargs='?', help='absolute path to an input file')
	return parser.parse_args(args)


def main():
	parser = parse_args(sys.argv[1:])

	# Open from file if supplied, else from stdin.
	lines = open(parser.file) if parser.file else sys.stdin

	handler = TopRecordHandler(parser.x_largest)
	for line in lines:
		record = Record(line)
		handler.add(record)

	handler.output()

	#　Close file if it was supplied.
	if lines: lines.close()


if __name__ == '__main__':
	main()  # pragma: no cover
