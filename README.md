# Group Assign (Python)

This is a script to distribute group problems for [CSCI425](https://cs.mcprogramming.com/comp/)
at Mines. It can distribute problems fairly, with each problem (optionally)
being solved my multiple students. It uses the [OR-Tools](https://developers.google.com/optimization)
CP-SAT Solver.

## Usage

```bash
uv run main.py <problem count> <group members, separated by commas> [--coverage 2]
```
