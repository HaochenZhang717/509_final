def unit_propagate(clauses, assignment):
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            break

        for unit in unit_clauses:
            literal = unit[0]
            var = abs(literal)
            val = literal > 0

            if var in assignment:
                if assignment[var] != val:
                    return None, None
                continue  # skip redundant
            assignment[var] = val

            # Update clauses
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue  # satisfied
                if -literal in clause:
                    new_clause = [x for x in clause if x != -literal]
                    if not new_clause:
                        return None, None
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(clause)
            clauses = new_clauses  # important: update after each unit

    return clauses, assignment





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
    new_variables_chosen = variables_chosen + [variable_]

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
