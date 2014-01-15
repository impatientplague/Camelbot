import json
import bank

with open('data/users.json') as f:
	db = json.load(f)


def check(uname):
	if uname in db['accounts']:
		return True
	else:
		return False

