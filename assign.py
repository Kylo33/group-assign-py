from ortools.sat.python import cp_model
from collections import defaultdict
import random

import click

@click.command()
@click.argument("problems", type=int)
@click.argument("group")
def main(problems: int, group: str):
    group = group.split(",")
    random.shuffle(group)

    model = cp_model.CpModel()

    # each problem should be solved by two different people
    member_vars = defaultdict(list)
    for problem in range(1, problems + 1):
        problem_vars = []
        for name in group:
            pnamevar = model.new_int_var(0, 1, f"p{problem}:{name}")
            problem_vars.append(pnamevar)
            member_vars[name].append(pnamevar)

        random.shuffle(problem_vars)
        model.Add(sum(problem_vars) == 2)

    # nobody should have more than 1 problem more than another person
    for person1 in group:
        for person2 in group:
            if person1 == person2:
                continue

            model.Add(sum(member_vars[person1]) - sum(member_vars[person2]) <= 1)
            model.Add(sum(member_vars[person2]) - sum(member_vars[person1]) <= 1)

    solver = cp_model.CpSolver()
    solver.solve(model)

    group.sort()

    # print the results
    for member in group:
        assignments = []
        for problem_number, var in enumerate(member_vars[member], start=1):
            if solver.value(var) == 1:
                assignments.append(problem_number)

        print(f"{member}: {','.join(map(str, assignments))}")

if __name__ == "__main__":
    main()
