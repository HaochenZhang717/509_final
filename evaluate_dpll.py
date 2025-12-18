import os
import random
import statistics
import numpy as np
from time import time
from solver import dpll
from random_problem_gen import generate_random_3sat_instance

import multiprocessing as mp
from time import time
from solver import dpll
import json


def _dpll_worker(clauses, heuristic, return_dict):
    global dpll_calls
    dpll_calls = 0
    try:
        solution = dpll(clauses, heuristics_type=heuristic)
        return_dict['solution'] = solution
        return_dict['calls'] = dpll_calls
    except RecursionError:
        return_dict['solution'] = None
        return_dict['calls'] = None


def run_experiment(N, L, heuristic, timeout=5):
    clauses = generate_random_3sat_instance(N, L, seed=random.randint(0, int(1e9)))
    manager = mp.Manager()
    return_dict = manager.dict()

    p = mp.Process(target=_dpll_worker, args=(clauses, heuristic, return_dict))
    start_time = time()
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return None, None, False  # Timeout

    elapsed = time() - start_time
    solution = return_dict.get('solution', None)
    calls = return_dict.get('calls', None)
    is_sat = solution is not None

    return elapsed, calls, is_sat


def run_all(N_list=[100, 150], L_N_range=np.arange(3.0, 6.2, 0.2), num_trials=100):
    results = {}

    for N in N_list:
        print(f"Running for N = {N}")
        results[N] = {}

        for L_N in L_N_range:
            L = int(L_N * N)
            print(f"  L/N = {L_N:.1f} (L = {L})")
            stats = {
                "random": {"times": [], "calls": [], "sats": 0},
                "2_clause_heuristics": {"times": [], "calls": [], "sats": 0},
                "mine": {"times": [], "calls": [], "sats": 0},
            }

            for trial in range(num_trials):
                for heuristic in stats.keys():
                    t, calls, is_sat = run_experiment(N, L, heuristic)

                    if t is not None:
                        stats[heuristic]["times"].append(t)
                        stats[heuristic]["calls"].append(calls)
                        if is_sat:
                            stats[heuristic]["sats"] += 1

            # summarize
            results[N][L_N] = {
                h: {
                    "median_time": statistics.median(v["times"]) if v["times"] else None,
                    "median_calls": statistics.median(v["calls"]) if v["calls"] else None,
                    "sat_prob": v["sats"] / num_trials,
                } for h, v in stats.items()
            }
    output_path = "dpll_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Saved results to {output_path}")
    return results


if __name__ == "__main__":
    run_all()