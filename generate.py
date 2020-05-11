import sys
import random

if __name__ == "__main__":
	quantity = int(sys.argv[1])
	outfile = f'{quantity}.txt'
	out = open(outfile, 'w')
	for i in range(1, quantity + 1):
		uid = str(i).zfill(9)
		value = random.randint(1, quantity)
		out.write(f'{uid} {value}\n')
	out.close()
