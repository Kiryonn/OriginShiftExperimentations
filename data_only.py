from _typeshed import SupportsWrite
from typing import Callable, Literal


class Bcolors:
	BLUE = '\033[94m'
	BOLD = '\033[1m'
	CYAN = '\033[96m'
	END = '\033[0m'
	FAIL = '\033[91m'
	GREEN = '\033[92m'
	HEADER = '\033[95m'
	UNDERLINE = '\033[4m'
	WARNING = '\033[93m'

def print_err(*values: str, sep=' ', end='\n', file: SupportsWrite[str] | None = None, flush: Literal[False] = False):
	print('\033[91m', end='', file=file)
	print(*values, sep=sep, end='', file=file)
	print('\033[0m', end=end)


def print_help():
	pass


def print_results():
	pass


def start_test(test_name: str, nb_ars):
	pass


def __detect_cmd(input_str: str) -> tuple[Callable, list] | None:
	pass


if __name__ == '__main__':
	is_running = True
	print("type help() to get help")
	while is_running:
		cmd = __detect_cmd(input())
		if cmd is None:
			print_err("")
			continue
