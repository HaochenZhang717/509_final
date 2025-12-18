from solver import read_dimacs, dpll
from encode_problem import encode_problem, decode_solution
from time import time


encode_problem()
num_vars, clauses = read_dimacs("my_einstein.cnf")

start = time()
solution = dpll(clauses, heuristics_type="random")
end = time()
print("running time: ", end - start)
# print("solution: ", decode_solution(solution))
#------------------------------------
start = time()
solution = dpll(clauses, heuristics_type="2_clause_heuristics")
end = time()
print("running time: ", end - start)
# print("solution: ", decode_solution(solution))
#------------------------------------
start = time()
solution = dpll(clauses, heuristics_type="mine")
end = time()
print("running time: ", end - start)
# print("solution: ", decode_solution(solution))



# print(solution)
if solution:
    print("SAT")
    house_info = decode_solution(solution)
else:
    print("UNSAT")