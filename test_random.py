from solver import read_dimacs, dpll
from time import time
import statistics


def print_stats(times, label):
    mean_time = statistics.mean(times)
    median_time = statistics.median(times)
    print(f"{label}:")
    print(f"  Mean   = {mean_time:.4f} s")
    print(f"  Median = {median_time:.4f} s")
    print()

# num_vars, clauses = read_dimacs("random_3sat_n100_l630.cnf")
# random_times = []
# two_clause_heuristics_times = []
# my_times = []
# print("-----------------------------------"*5)
# print(100)
# for iteration in range(5):
#     print(f"{iteration+1}/5")
#     start = time()
#     solution_1 = dpll(clauses, heuristics_type="random")
#     end = time()
#     random_time = end - start
#     random_times.append(random_time)
#     # print("running time: ", end - start)
#     # print("solution: ", decode_solution(solution))
#     #------------------------------------
#     start = time()
#     solution_2 = dpll(clauses, heuristics_type="2_clause_heuristics")
#     end = time()
#     two_clause_heuristics_time = end - start
#     two_clause_heuristics_times.append(two_clause_heuristics_time)
#     # print("running time: ", end - start)
#     # print("solution: ", decode_solution(solution))
#     #------------------------------------
#     start = time()
#     solution_3 = dpll(clauses, heuristics_type="mine")
#     end = time()
#     my_time = end - start
#     my_times.append(my_time)
#     # print("running time: ", end - start)
#
# print_stats(random_times, "Random Heuristic")
# print_stats(two_clause_heuristics_times, "2-Clause Heuristic")
# print_stats(my_times, "My Heuristic")
#
# print("-----------------------------------"*5)
# print("-----------------------------------"*5)
# print("-----------------------------------"*5)
# print("-----------------------------------"*5)

# encode_problem()
num_vars, clauses = read_dimacs("random_3sat_n150_l630.cnf")
random_times = []
two_clause_heuristics_times = []
my_times = []
print("-----------------------------------"*5)
print(150)
for iteration in range(1):
    print(f"{iteration+1}/5")
    start = time()
    solution_1 = dpll(clauses, heuristics_type="random")
    end = time()
    random_time = end - start
    random_times.append(random_time)
    print("running time: ", end - start)
    # print("solution: ", decode_solution(solution))
    #------------------------------------
    start = time()
    solution_2 = dpll(clauses, heuristics_type="2_clause_heuristics")
    end = time()
    two_clause_heuristics_time = end - start
    two_clause_heuristics_times.append(two_clause_heuristics_time)
    print("running time: ", end - start)
    # print("solution: ", decode_solution(solution))
    #------------------------------------
    start = time()
    solution_3 = dpll(clauses, heuristics_type="mine")
    end = time()
    my_time = end - start
    my_times.append(my_time)
    print("running time: ", end - start)

print_stats(random_times, "Random Heuristic")
print_stats(two_clause_heuristics_times, "2-Clause Heuristic")
print_stats(my_times, "My Heuristic")
