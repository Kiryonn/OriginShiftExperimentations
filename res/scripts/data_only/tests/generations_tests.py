import timeit
import inspect
from typing import Callable

from res.scripts.data_only.algos.multi_origin_shift import generation_mos
from res.scripts.data_only.algos.multi_weighted_origin_shift import generation_mwos
from res.scripts.data_only.algos.origin_shift import generation_os
from res.scripts.data_only.algos.reversed_dfs import reversed_dfs
from res.scripts.data_only.algos.weighted_origin_shift import generation_wos
from res.scripts.data_only.utils import units, get_stats, neighbors
from res.scripts.generic.signals import Signal


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
	gen_funcs: dict[str, Callable] = {
		"Reversed DFS": reversed_dfs,
		"Origin Shift": generation_os,
		"Weighted Origin Shift": generation_wos,
		"Multi Origin Shift": generation_mos,
		"Multi Weighted Origin Shift": generation_mwos
	}

	print(f"Testing {len(gen_funcs)} generation algorithms on a {size[0]}x{size[1]} maze over {nb_iterations} iterations...\n")
	sub_funcs: dict[str, count_calls] = {}
	test_funcs: dict[str, Callable] = {}
	for k in gen_funcs:
		p = inspect.signature(gen_funcs[k]).parameters
		if "algo" in p:
			subalgo = count_calls(p["algo"].default)
			sub_funcs[k] = subalgo
			test_funcs[k] = lambda g=gen_funcs[k],a=subalgo: g(size, algo=a)
		else:
			test_funcs[k] = lambda g=gen_funcs[k]: g(size)

	res = {
		"timings": { k: [0.0] * nb_iterations for k in gen_funcs },
		"nb calls": { k: [0] * nb_iterations for k in sub_funcs }
	}

	for i in range(nb_iterations):
		on_progression_changed.emit(progression=i / nb_iterations)

		for k in sub_funcs:
			sub_funcs[k].nb_calls = 0
		for k in test_funcs:
			res["timings"][k][i] = timeit.timeit(test_funcs[k], globals=locals(), number=1)
			neighbors.cache_clear()
			if k in sub_funcs:
				res["nb calls"][k][i] = sub_funcs[k].nb_calls
	on_progression_changed.emit(progression=1)
	return res
