import sys

if __name__ == "__main__":
	num_of_stairs = int(sys.argv[1])
	stairs = [' '] * num_of_stairs
	for i in range(1, num_of_stairs+1):
		stairs[-i] = '#'
		print(''.join(stairs))