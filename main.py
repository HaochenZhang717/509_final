def unit_propagate(clauses, assignment):
    """
    Perform unit propagation on the clauses.
    `clauses` is a list of lists, each inner list is a clause.
    `assignment` is a dict {var: True/False}
    """
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for clause in unit_clauses:
            literal = clause[0]
            var = abs(literal)
            val = literal > 0  # True if positive literal, else False

            # If inconsistency: variable already assigned opposite value
            if var in assignment and assignment[var] != val:
                return None, None  # contradiction

            assignment[var] = val
            changed = True

            # Simplify clauses
            new_clauses = []
            for c in clauses:
                if literal in c:
                    continue  # clause satisfied
                if -literal in c:
                    new_c = [x for x in c if x != -literal]  # remove negation
                    if len(new_c) == 0:
                        return None, None
                    new_clauses.append(new_c)
                else:
                    new_clauses.append(c)

            clauses = new_clauses
    return clauses, assignment


def DPLL(clauses, assignment=None):
    """
    clauses: list of clauses, e.g. [[1, -2], [2, 3], [-1]]
    assignment: dict {variable: Boolean}
    """
    if assignment is None:
        assignment = {}

    # Step 1: Unit Propagation
    clauses, assignment = unit_propagate(clauses, assignment)
    if clauses is None:
        return None  # UNSAT

    if not clauses:  # no clauses left → SAT
        return assignment

    # Step 2: Pick a literal to branch on (just choose first literal)
    literal = clauses[0][0]
    var = abs(literal)

    # Try True
    new_assignment = assignment.copy()
    new_assignment[var] = True
    result = DPLL([c.copy() for c in clauses] + [[var]], new_assignment)
    if result is not None:
        return result

    # Try False
    new_assignment = assignment.copy()
    new_assignment[var] = False
    result = DPLL([c.copy() for c in clauses] + [[-var]], new_assignment)
    if result is not None:
        return result

    return None  # no solution, UNSAT


import random


def choose_literal(clauses, variables_chosen, heuristics_type="random"):
    # Random-choice heuristic: return a random literal (with sign)
    if heuristics_type == "random":
        random_clause = random.choice(clauses)
        random_literal = random.choice(random_clause)
        return random_literal

    # 2-clause heuristic: choose a literal whose variable appears most in 2-clauses
    if heuristics_type == "2_clause_heuristics":
        appearance_times = {}
        for clause in clauses:
            if len(clause) == 2:
                for literal in clause:
                    var = abs(literal)
                    appearance_times[var] = appearance_times.get(var, 0) + 1

        if appearance_times:
            # Find variable with max appearance
            max_var = max(appearance_times, key=appearance_times.get)

            # Return a literal for that variable (choose a sign)
            return max_var  # return +var as literal

        # If no 2-clauses exist → fallback to random
        return choose_literal(clauses, variables_chosen, heuristics_type="random")

    # Your own heuristic: first literal with an unchosen variable
    if heuristics_type == "mine":
        for clause in clauses:
            for literal in clause:
                var = abs(literal)
                if var not in variables_chosen:
                    return literal

    # Default fallback
    return clauses[0][0]


# -------------------- TEST --------------------
if __name__ == "__main__":
    # (x1 ∨ ¬x2) ∧ (x2) ∧ (¬x1 ∨ x3)
    formula = [
        [1, -2],
        [2],
        [-1, 3]
    ]

    sol = DPLL(formula)
    print("SAT Solution:" if sol else "UNSAT", sol)







# function DPLL(clauses, assignment):
#
#     // 第一步：做单子句传播
#     (clauses, assignment) = unit_propagate(clauses, assignment)
#     如果传播返回 None → 返回 UNSAT
#
#     // 第二步：检查是否完成
#     如果 clauses 为空 → 所有子句都满足 → 返回 assignment 作为解
#
#     // 第三步：选一个变量用于分裂
#     从某个子句中挑一个 literal，取出变量 var
#
#     // 第四步：分两种情况递归
#     尝试 var = True:
#         新建 assignment 副本，加入 var=True
#         把这个赋值加成单子句加入 clauses
#         调用 DPLL(...)
#         如果返回解，不是 UNSAT，则直接返回
#
#     尝试 var = False:
#         同样操作
#
#     // 如果两种都不行 → 无解
#     返回 UNSAT