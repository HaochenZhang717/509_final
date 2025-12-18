import random


def generate_random_3sat_instance(N, L, seed):

    random.seed(seed)

    clauses = []
    while len(clauses) < L:
        vars = random.sample(range(1, N + 1), 3)
        clause = []
        for v in vars:
            if random.random() < 0.5:
                clause.append(v)
            else:
                clause.append(-v)
        clauses.append(clause)

    return clauses


def write_cnf_to_dimacs(clauses, N, filename):
    with open(filename, 'w') as f:
        f.write(f"p cnf {N} {len(clauses)}\n")
        for clause in clauses:
            clause_line = ' '.join(str(lit) for lit in clause) + " 0\n"
            f.write(clause_line)


if __name__ == "__main__":
    # Example usage
    N = 150  # Number of variables
    L = 630  # Number of clauses (L/N = 4.2 → phase transition)
    seed = 0  # For reproducibility

    clauses = generate_random_3sat_instance(N, L, seed)
    write_cnf_to_dimacs(clauses, N, "random_3sat_n150_l630.cnf")