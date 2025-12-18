from rdflib.plugins.parsers.ntriples import literal

category_values = {
    "Color": ["Red", "Green", "White", "Yellow", "Blue"],
    "Nationality": ["Brit", "Swede", "Dane", "Norwegian", "German"],
    "Drink": ["Tea", "Coffee", "Milk", "Beer", "Water"],
    "Cigarette": ["PallMall", "Dunhill", "Blends", "Prince", "BlueMaster"],
    "Pet": ["Dog", "Bird", "Cat", "Horse", "Fish"]
}

num_houses = 5

var_id = {}
id_idx = 1
clauses = []


def create_variables():
    global id_idx
    for cat, values in category_values.items():
        for value_ in values:
            for i in range(1, num_houses+1):
                var_id[(cat, value_, i)] = id_idx
                id_idx += 1

def add_constraint(literals):
    clauses.append(literals)
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            clauses.append([-literals[i], -literals[j]])


def add_constraints_house():
    for i in range(1, num_houses + 1):
        for cat, values in category_values.items():
            literals = []
            for value_ in values:
                literals.append(var_id[(cat, value_, i)])
            add_constraint(literals)


def add_constraints_unique():
    for cat, values in category_values.items():
        for value_ in values:
            literals = []
            for i in range(1, num_houses + 1):
                literals.append(var_id[(cat, value_, i)])
            add_constraint(literals)


def add_clauses():
    #1) The Brit lives in the Red house.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Nationality", "Brit", i)], var_id[("Color", "Red", i)]])

    #2) The Swede keeps dogs.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Nationality", "Swede", i)], var_id[("Pet", "Dog", i)]])

    #3) The Dane drinks tea.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Nationality", "Dane", i)], var_id[("Drink", "Tea", i)]])

    #4) The green house is immediately to the left of the white house.
    for i in range(1, num_houses):   # 1 to 4
        clauses.append([-var_id[("Color", "Green", i)], var_id[("Color", "White", i + 1)]])
    for i in range(2, num_houses + 1):  # 2 to 5
        clauses.append([-var_id[("Color", "White", i)], var_id[("Color", "Green", i - 1)]])

    #5) The owner of the green house drinks coffee.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Color", "Green", i)], var_id[("Drink", "Coffee", i)]])

    #6) The person who smokes PallMall rears birds.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Cigarette", "PallMall", i)], var_id[("Pet", "Bird", i)]])

    #7) The owner of the yellow house smokes Dunhill.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Color", "Yellow", i)], var_id[("Cigarette", "Dunhill", i)]])

    #8) The man living in the center house drinks milk. (House 3)
    clauses.append([var_id[("Drink", "Milk", 3)]])

    #9) The Norwegian lives in the first house.
    clauses.append([var_id[("Nationality", "Norwegian", 1)]])


    #10) The man who smokes Blends lives next to the one who keeps cats.
    for i in range(1, num_houses + 1):
        neighbors = []
        if i - 1 >= 1:
            neighbors.append(var_id[("Pet", "Cat", i - 1)])
        if i + 1 <= num_houses:
            neighbors.append(var_id[("Pet", "Cat", i + 1)])
        clauses.append([-var_id[("Cigarette", "Blends", i)]] + neighbors)

    #11) The man who keeps horses lives next to the man who smokes Dunhill.
    for i in range(1, num_houses + 1):
        neighbors = []
        if i - 1 >= 1:
            neighbors.append(var_id[("Cigarette", "Dunhill", i - 1)])
        if i + 1 <= num_houses:
            neighbors.append(var_id[("Cigarette", "Dunhill", i + 1)])
        clauses.append([-var_id[("Pet", "Horse", i)]] + neighbors)

    #12) The owner who smokes BlueMaster drinks beer.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Cigarette", "BlueMaster", i)], var_id[("Drink", "Beer", i)]])

    #13) The German smokes Prince.
    for i in range(1, num_houses + 1):
        clauses.append([-var_id[("Nationality", "German", i)], var_id[("Cigarette", "Prince", i)]])

    #14) The Norwegian lives next to the blue house.
    for i in range(1, num_houses + 1):
        neighbors = []
        if i - 1 >= 1:
            neighbors.append(var_id[("Color", "Blue", i - 1)])
        if i + 1 <= num_houses:
            neighbors.append(var_id[("Color", "Blue", i + 1)])
        clauses.append([-var_id[("Nationality", "Norwegian", i)]] + neighbors)

    #15) The man who smokes Blends has a neighbor who drinks water.
    for i in range(1, num_houses + 1):
        neighbors = []
        if i - 1 >= 1:
            neighbors.append(var_id[("Drink", "Water", i - 1)])
        if i + 1 <= num_houses:
            neighbors.append(var_id[("Drink", "Water", i + 1)])
        clauses.append([-var_id[("Cigarette", "Blends", i)]] + neighbors)


def export_dimacs():
    with open("my_einstein.cnf", "w") as f:
        f.write(f"p cnf {id_idx - 1} {len(clauses)}\n")
        for clause in clauses:
            line = " ".join(str(x) for x in clause) + " 0\n"
            f.write(line)

def decode_solution(assignment):
    reverse_var = {v: k for k, v in var_id.items()}

    house_info = {i: {} for i in range(1, num_houses + 1)}

    for var, value in assignment.items():
        if value is True:     # 只看 True 的变量
            cat, val, house = reverse_var[var]
            house_info[house][cat] = val

    for key, value in house_info.items():
        print(key)
        print(value)
        print("-"*60)
    return house_info

def encode_problem():
    create_variables()
    add_constraints_house()
    add_constraints_unique()
    add_clauses()
    export_dimacs()
