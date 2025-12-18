from copy import deepcopy
import random
import sys
sys.setrecursionlimit(500000)  # 或更大

def unit_propagate(clauses, assignment):
    while True:
        new_change = False
        unit_clauses = []
        for clause in clauses:
            if len(clause) == 1:
                unit_clauses.append(clause)
        if len(unit_clauses) == 0:
            break

        for unit_clause in unit_clauses:
            literal = unit_clause[0]
            variable_ = abs(literal)
            value_ = (literal > 0)

            if variable_ in assignment:
                if assignment[variable_] != value_:
                    return None, None
                continue  #
            assignment[variable_] = value_

            new_clauses = []
            for clause in clauses:
                if -literal in clause:
                    new_clause = []
                    for x in clause:
                        if x != -literal:
                            new_clause.append(x)
                    if not new_clause:
                        return None, None
                    new_clauses.append(new_clause)
                elif literal in clause:
                    continue
                else:
                    new_clauses.append(clause)
            clauses = new_clauses


    return clauses, assignment



def choose_literal(clauses, variables_chosen, heuristics_type="random"):
    all_variables = set(abs(lit) for clause in clauses for lit in clause)
    candidates = list(all_variables - set(variables_chosen))

    if len(candidates) == 0:
        return random.choice(list(all_variables))  # fallback


    if heuristics_type == "random":
        random_literal = random.choice(candidates)
        return random_literal

    if heuristics_type == "2_clause_heuristics":
        appearance_times = {}
        for clause in clauses:
            if len(clause) == 2:
                for literal in clause:
                    variable_ = abs(literal)
                    if variable_ not in variables_chosen:
                        appearance_times[variable_] = appearance_times.get(variable_, 0) + 1

        if appearance_times:
            max_frequency = max(appearance_times.values())
            best_variables = [v for v, freq in appearance_times.items() if freq == max_frequency]
            return random.choice(best_variables)
        else:
            return random.choice(candidates)


    if heuristics_type == "mine":
        appearance_times = {}
        for clause in clauses:
            for literal in clause:
                if abs(literal) not in variables_chosen:
                    appearance_times[abs(literal)] = appearance_times.get(abs(literal), 0) + 1 / len(clause)

        if appearance_times:
            max_score = max(appearance_times.values())
            best_variables = [v for v, score in appearance_times.items() if score == max_score]
            return random.choice(best_variables)
        else:
            return random.choice(candidates)



def dpll(clauses, assignment=None, variables_chosen=None, heuristics_type="random"):
    if assignment is None:
        assignment = {}

    if variables_chosen is None:
        variables_chosen = []

    clauses, assignment = unit_propagate(clauses, assignment)

    if clauses is None:
        return None

    if clauses == []:
        return assignment

    variable_ = choose_literal(clauses, variables_chosen, heuristics_type=heuristics_type)
    new_variables_chosen = variables_chosen.copy()
    new_variables_chosen = new_variables_chosen + [variable_]

    for sign in [True, False]:
        new_assignment = deepcopy(assignment)
        new_assignment[variable_] = sign

        output = dpll(
            deepcopy(clauses),
            new_assignment,
            variables_chosen=new_variables_chosen,
            heuristics_type=heuristics_type
        )
        if output is not None:
            return output

    return None


def read_dimacs(path):
    num_vars = 0
    clauses = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                _, _, num_vars, _ = line.split()
                num_vars = int(num_vars)
            else:
                clause = list(map(int, line.split()[:-1]))  # remove trailing 0
                clauses.append(clause)
    return num_vars, clauses


if __name__ == "__main__":
    formula = [
        [1, -2],
        [2],
        [-1, 3]
    ]

    sol = dpll(formula)
    print("SAT Solution:" if sol else "UNSAT", sol)