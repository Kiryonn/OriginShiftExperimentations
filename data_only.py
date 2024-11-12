import json
import os
import sys

from res.scripts.data_only.tests import generations_tests


def print_progression(progression: float):
	percent = progression * 100
	num_blocks = int(percent * 0.5)
	sys.stdout.write(f"\rProgress: [{"#" * num_blocks}{" " * (50 - num_blocks)}] {percent:.1f}%")
	sys.stdout.flush()


def start_test(show_res: bool = False, output: str = None, *args, **kws):
	# this section only prevent users from waiting results just to get a file error at the end
	if output is not None:
		folder = os.path.dirname(output)
		if folder != '': os.makedirs(folder, exist_ok=True)
		open(output, "w", encoding="utf-8").close()

	# start tests
	generations_tests.on_progression_changed += print_progression
	results = generations_tests.start(*args, **kws)
	generations_tests.on_progression_changed -= print_progression
	print('\n') # put some space after progression bar


	if show_res:
		generations_tests.result_printer(results)

	if output is not None:
		folder = os.path.dirname(output)
		if folder != '': os.makedirs(folder, exist_ok=True)
		with open(output, "w", encoding="utf-8") as file: json.dump(results, file, indent='\t')
		print(f"\nSaved results to file at {os.path.abspath(output)}")


def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--size", nargs=2, type=int, help="the size of the maze")
	parser.add_argument("-i", "--iter", default=1000, type=int, help="the number of iterations")
	parser.add_argument("-r", "--show_res", action="store_true", help="shows a summary of the results")
	parser.add_argument('-o', '--output', default=None, help="saves the results in a specified file")
	namespace = parser.parse_args()
	args = [namespace.show_res, namespace.output]
	kws = {"size": tuple(namespace.size), "nb_iterations": namespace.iter}
	start_test(*args, **kws)


if __name__ == "__main__":
	main()
