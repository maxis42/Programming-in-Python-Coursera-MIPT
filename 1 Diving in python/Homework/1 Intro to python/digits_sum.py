import sys

if __name__ == "__main__":
	digit_string = sys.argv[1]
	digit_sum = sum([int(x) for x in digit_string])

	print(digit_sum)
