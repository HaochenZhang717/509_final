# test_parallel.py
import random
import statistics
import numpy as np
import multiprocessing as mp
import json
import time

from solver import dpll
from random_problem_gen import generate_random_3sat_instance
import solver

def run_single_trial(args):
    N, L, heuristic, timeout = args

    clauses = generate_random_3sat_instance(
        N, L, seed=random.randint(0, 10**9)
    )

    solver.dpll_calls = 0
    start = time.time()


    solution = dpll(clauses, heuristics_type=heuristic)

    elapsed = time.time() - start
    if elapsed > timeout:
        elapsed = None
        calls = None
        is_sat = None
        return heuristic, elapsed, calls, is_sat

    calls = solver.dpll_calls
    is_sat = solution is not None

    return heuristic, elapsed, calls, is_sat



def run_all_parallel(
    N_list=(100, 150),
    L_N_range=np.arange(3.0, 6.0, 0.2),
    num_trials=100,
    timeout=1,
    num_workers=None,
):
    if num_workers is None:
        num_workers = mp.cpu_count()
    print("Num workers:", num_workers)

    results = {}

    for N in N_list:
        print(f"N = {N}")
        results[N] = {}

        for L_N in L_N_range:
            L = int(L_N * N)
            print(f"  L/N = {L_N} (L = {L})")

            stats = {
                "random": {"times": [], "calls": [], "sats": 0},
                "2_clause_heuristics": {"times": [], "calls": [], "sats": 0},
                "mine": {"times": [], "calls": [], "sats": 0},
            }

            # prepare jobs
            jobs = []
            for _ in range(num_trials):
                for heuristic in stats.keys():
                    jobs.append((N, L, heuristic, timeout))

            with mp.Pool(processes=num_workers) as pool:
                for heuristic, t, calls, is_sat in pool.imap_unordered(
                    run_single_trial, jobs
                ):
                    if t is not None:
                        stats[heuristic]["times"].append(t)
                        stats[heuristic]["calls"].append(calls)
                        if is_sat:
                            stats[heuristic]["sats"] += 1

            # summarize
            results[N][L_N] = {
                h: {
                    "median_time": statistics.median(v["times"])
                    if v["times"] else None,
                    "median_calls": statistics.median(v["calls"])
                    if v["calls"] else None,
                    "sat_prob": v["sats"] / num_trials,
                }
                for h, v in stats.items()
            }

    # save results
    with open("dpll_results_parallel_4.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    run_all_parallel()