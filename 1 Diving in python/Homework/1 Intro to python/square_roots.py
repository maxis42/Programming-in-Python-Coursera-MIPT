import sys

if __name__ == "__main__":
	a = int(sys.argv[1])
	b = int(sys.argv[2])
	c = int(sys.argv[3])
	
	diskr = b**2 - 4*a*c
	x1 = (-b + diskr**0.5)/(2*a)
	x2 = (-b - diskr**0.5)/(2*a)
	
	print(int(x1))
	print(int(x2))
