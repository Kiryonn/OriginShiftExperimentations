import timeit
from typing import Callable

from res.scripts.data_only.algos.multi_origin_shift import multi_origins_shift, generation_mos
from res.scripts.data_only.algos.origin_shift import origin_shift, generation_os
from res.scripts.data_only.algos.reversed_dfs import reversed_dfs
from res.scripts.data_only.algos.weighted_origin_shift import weighted_origin_shift, generation_wos
from res.scripts.data_only.utils import units, get_stats
from res.scripts.signals import Signal


def count_calls(func: Callable):
	def wrapper(*args, **kws):
		wrapper.nb_calls += 1
		return func(*args, **kws)

	wrapper.nb_calls = 0
	return wrapper


on_progression_changed = Signal()


# noinspection SpellCheckingInspection
def result_printer(results: dict[str, dict[str, list]]):
	headers = ["Evaluation"]
	headers.extend(results["timings"].keys())

	timings_stats = [get_stats(results["timings"][algo]) for algo in headers[1:]]
	maxs = [x["max"] for x in timings_stats]

	unit_index = 0
	multiplier = lambda e: e * 1000**unit_index
	while unit_index < len(units)-1 and int(max(map(multiplier, maxs))) < 10:
		unit_index += 1

	time_unit = units[unit_index]
	mins = [round(multiplier(n), 2) for n in [x["min"] for x in timings_stats]]
	maxs = [round(multiplier(n), 2) for n in maxs]
	means = [round(multiplier(n), 2) for n in [x["mean"] for x in timings_stats]]
	q1s = [round(multiplier(n), 2) for n in [x["q1"] for x in timings_stats]]
	q3s = [round(multiplier(n), 2) for n in [x["q3"] for x in timings_stats]]

	table = [
		[f"Timings (in {time_unit})"] + [""] * (len(headers) - 1),
		["Min"] + mins,
		["Max"] + maxs,
		["Mean"] + means,
		["Q1"] + q1s,
		["Q3"] + q3s
	]

	calls_stats = [get_stats(results["nb calls"].get(algo, [])) for algo in headers[1:]]
	table.extend([
		[""] * len(headers),
		["Nb Calls"] + [""] * (len(headers) - 1),
		["Min"] + [x["min"] for x in calls_stats],
		["Max"] + [x["max"] for x in calls_stats],
		["Mean"] + [x["mean"] for x in calls_stats],
		["Q1"] + [x["q1"] for x in calls_stats],
		["Q3"] + [x["q3"] for x in calls_stats]
	])
	from tabulate import tabulate
	print(tabulate(table, headers=headers))


# noinspection SpellCheckingInspection
def start(size: tuple[int, int] = (16, 16), nb_iterations=1000):
	print(f"Testing 4 generation algorithms on a {size[0]}x{size[1]} maze over {nb_iterations} iterations...")
	ccos = count_calls(origin_shift)
	ccwos = count_calls(weighted_origin_shift)
	ccmos = count_calls(multi_origins_shift)

	grdfs = lambda: reversed_dfs(size)
	gos = lambda: generation_os(size, algo=ccos)
	gwos = lambda: generation_wos(size, algo=ccwos)
	gmos = lambda: generation_mos(size, algo=ccmos)

	res = {
		"timings": {
			"Reversed DFS": [0.0] * nb_iterations,
			"Origin Shift": [0.0] * nb_iterations,
			"Weighted Origin Shift": [0.0] * nb_iterations,
			"Multi Origin Shift (incomplete)": [0.0] * nb_iterations
		},
		"nb calls": {
			"Origin Shift": [0] * nb_iterations,
			"Weighted Origin Shift": [0] * nb_iterations,
			"Multi Origin Shift (incomplete)": [0] * nb_iterations
		}
	}

	for i in range(nb_iterations):
		on_progression_changed.emit(progression=i / nb_iterations)
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
	on_progression_changed.emit(progression=1)
	return res


if __name__ == "__main__":
	start()
