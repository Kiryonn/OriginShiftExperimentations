def isint(value: str, base=10):
	try:
		int(value, base)
		return True
	except ValueError:
		return False


def isfloat(value: str):
	try:
		float(value)
		return True
	except ValueError:
		return False
