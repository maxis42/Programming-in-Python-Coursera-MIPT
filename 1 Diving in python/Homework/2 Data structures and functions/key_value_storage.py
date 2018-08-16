import os
import tempfile
import argparse
import json


# command line arguments parser
parser = argparse.ArgumentParser()
parser.add_argument('--key')
parser.add_argument('--val')
args = parser.parse_args()


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
# storage_path = 'storage.data'

if os.path.isfile(storage_path):
	with open(storage_path, 'r') as f:
		data = json.load(f)
	if args.val:
		if args.key in data:
			data[args.key].append(args.val)
		else:
			data[args.key] = [args.val]
		with open(storage_path, 'w') as f:
			json.dump(data, f)
	else:
		if args.key in data:
			values = ', '.join(data[args.key])
			print(values)
		else:
			print(None)
else:
	with open(storage_path, 'w') as f:
		json.dump({}, f)