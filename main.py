from ortools.sat.python import cp_model
from collections import defaultdict
import random

import click

@click.command()
@click.argument("problems", type=int)
@click.argument("group")
@click.option("--coverage", default=2, help="Number of solvers per problem.")
def main(problems: int, group: str, coverage: int):
    group = group.split(",")

    assignments = assign_problems(problems, len(group), coverage)

    random.shuffle(group)
    answer = list(sorted(zip(group, assignments)))
    for person, problems in answer:
        click.echo(f"{person}: {problems}")

def assign_problems(problems: int, group_size: int, coverage: int) -> list[list[int]]:
    model = cp_model.CpModel()
    member_vars = [[] for _ in range(group_size)]

    # create problem assignment variables
    for problem in range(1, problems + 1):
        problem_vars = []
        for i in range(group_size):
            # 1 if this problem is assigned to this person, else 0
            pnamevar = model.new_int_var(0, 1, f"p{problem}:{i}")

            problem_vars.append(pnamevar)
            member_vars[i].append(pnamevar)

        # each problem should be solved by multiple different people
        model.Add(sum(problem_vars) == coverage)

    # nobody should have more than 1 problem more than another person
    for i in range(group_size):
        for j in range(group_size):
            if i == j:
                continue

            model.Add(sum(member_vars[i]) - sum(member_vars[j]) <= 1)
            model.Add(sum(member_vars[i]) - sum(member_vars[j]) >= -1)

    solver = cp_model.CpSolver()
    solver.solve(model)

    ret = []
    for i in range(group_size):
        ret.append([])
        for problem_number, var in enumerate(member_vars[i], start=1):
            if solver.value(var) == 1:
                ret[-1].append(problem_number)

    return ret

if __name__ == "__main__":
    main()
