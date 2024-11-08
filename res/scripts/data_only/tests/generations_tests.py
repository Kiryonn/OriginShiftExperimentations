import json
import os
import timeit
from typing import Callable

from data_only import reversed_dfs, generation_os, generation_wos, generation_mos, origin_shift, \
	weighted_origin_shift, multi_origins_shift


def count_calls(func: Callable):
	def wrapper(*args, **kws):
		wrapper.nb_calls += 1
		return func(*args, **kws)

	wrapper.nb_calls = 0
	return wrapper


# noinspection SpellCheckingInspection
def main():
	sizes = [(16, 16), (32, 32), (64, 64)]
	nb_iterations = 1000
	folder = "data/generation/"
	os.makedirs(folder, exist_ok=True)
	for size in sizes:
		ccos = count_calls(origin_shift)
		ccwos = count_calls(weighted_origin_shift)
		ccmos = count_calls(multi_origins_shift)

		grdfs = lambda: reversed_dfs(size)
		gos = lambda: generation_os(size, algo=ccos)
		gwos = lambda: generation_wos(size, algo=ccwos)
		gmos = lambda: generation_mos(size, algo=ccmos)

		res = {
			"timings": {
				"Reversed DFS": [0] * nb_iterations,
				"Origin Shift": [0] * nb_iterations,
				"Weighted Origin Shift": [0] * nb_iterations,
				"Multi Origin Shift (incomplete)": [0] * nb_iterations
			},
			"nb calls": {
				"Origin Shift": [0] * nb_iterations,
				"Weighted Origin Shift": [0] * nb_iterations,
				"Multi Origin Shift (incomplete)": [0] * nb_iterations
			}
		}

		for i in range(nb_iterations):
			ccos.nb_calls = 0
			ccwos.nb_calls = 0
			ccmos.nb_calls = 0
			res["timings"]["Reversed DFS"][i] = timeit.timeit(grdfs, globals=locals(), number=1)
			res["timings"]["Origin Shift"][i] = timeit.timeit(gos, globals=locals(), number=1)
			res["timings"]["Weighted Origin Shift"][i] = timeit.timeit(gwos, globals=locals(), number=1)
			res["timings"]["Multi Origin Shift (incomplete)"][i] = timeit.timeit(gmos, globals=locals(), number=1)
			res["nb calls"]["Origin Shift"][i] = ccos.nb_calls
			res["nb calls"]["Weighted Origin Shift"][i] = ccwos.nb_calls
			res["nb calls"]["Multi Origin Shift (incomplete)"][i] = ccmos.nb_calls

		with open(f"{folder}{size[0]}x{size[1]}.json", 'w') as file:
			json.dump(res, file, indent='\t')


if __name__ == "__main__":
	main()
