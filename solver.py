from copy import deepcopy
import random
dpll_calls = 0

def unit_propagate(clauses, assignment):
    while True:
        new_change = False
        unit_clauses = []
        for clause in clauses:
            if len(clause) == 1:
                unit_clauses.append(clause)

        for unit_clause in unit_clauses:
            literal = unit_clause[0]
            variable_ = abs(literal)
            value_ = (literal > 0)

            if variable_ in assignment and assignment[variable_] != value_:
                return None, None

            assignment[variable_] = value_
            new_change = True

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

        if not new_change:
            break

    return clauses, assignment


def choose_literal(clauses, variables_chosen, heuristics_type="random"):

    if heuristics_type == "random":
        random_clause = random.choice(clauses)
        random_literal = random.choice(random_clause)
        return random_literal

    if heuristics_type == "2_clause_heuristics":
        appearance_times = {}
        maximum_times = 0
        maximum_variable = None
        for clause in clauses:
            if len(clause) == 2:
                for literal in clause:
                    variable_ = abs(literal)
                    if variable_ in appearance_times.keys():
                        appearance_times[variable_] += 1
                    else:
                        appearance_times.update({variable_: 1})
                    if appearance_times[variable_] > maximum_times:
                        maximum_times = appearance_times[variable_]
                        maximum_variable = variable_
        if maximum_variable is not None:
            return maximum_variable
        else:
            return choose_literal(clauses, variables_chosen, heuristics_type="random")


    if heuristics_type == "mine":
        variable_scores = {}
        polarity_count = {}

        for clause in clauses:
            for literal in clause:
                var = abs(literal)
                if var in variables_chosen:
                    continue

                variable_scores[var] = variable_scores.get(var, 0) + 1 / len(clause)

                if literal > 0:
                    polarity_count[var] = polarity_count.get(var, [0, 0])
                    polarity_count[var][0] += 1
                else:
                    polarity_count[var] = polarity_count.get(var, [0, 0])
                    polarity_count[var][1] += 1

        if not variable_scores:
            return choose_literal(clauses, variables_chosen, heuristics_type="random")

        best_var = max(variable_scores.items(), key=lambda x: x[1])[0]

        pos, neg = polarity_count.get(best_var, [0, 0])
        return best_var if pos >= neg else -best_var

def dpll(clauses, assignment=None, variables_chosen=None, heuristics_type="random"):
    global dpll_calls
    dpll_calls += 1
    if assignment is None:
        assignment = {}

    if variables_chosen is None:
        variables_chosen = []

    clauses, assignment = unit_propagate(clauses, assignment)

    if clauses is None:
        return None

    if clauses == []:
        return assignment

    literal = choose_literal(clauses, variables_chosen, heuristics_type=heuristics_type)
    variable_ = abs(literal)
    # variables_chosen.append(variable_)
    new_variables_chosen = variables_chosen.copy()
    new_variables_chosen.append(variable_)


    new_assignment = deepcopy(assignment)
    new_assignment[variable_] = True
    output = dpll(deepcopy(clauses) + [[variable_]], new_assignment, variables_chosen=new_variables_chosen)
    if output is not None:
        return output

    new_assignment = deepcopy(assignment)
    new_assignment[variable_] = False
    output = dpll(deepcopy(clauses) + [[-variable_]], new_assignment, variables_chosen=variables_chosen)
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


