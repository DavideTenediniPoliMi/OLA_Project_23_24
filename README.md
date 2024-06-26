# OLA_Project_23_24

# THIS IS AN ABANDONED BRANCH. 
THE GOAL WAS TO BUILD A MODULAR SIMULATOR THAT COULD SIMULATE ALL THE REQUIREMENTS WITH ANY AGENT, JUST BY CHANGING A CONFIG FILE. UNFORTUNATELLY WE DIDN'T HAVE ENOUGH TIME AND WE RESORTED TO
USING SEPARATE NOTEBOOKS TO RUN THE EXPERIMENTS FOR EACH REQUIREMENT.


## Set-up
Clone the repo and `cd` into the folder.\
Make sure to have Python version `>=3.10`, and install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage
Change the parameters in `.\config\config.yaml` as you wish, then run a simulation with:

```bash
python simulation.py
```

The results of the simulation can be found in the folder `.\logger\logs\info\`. To clear the logs run:
```bash
python clear_logs.py
```

All the `.log` files inside `.\logger\logs\info\` and `.\logger\logs\debug\` will be deleted so if you wish to save some log file, move it to `.\logger\logs\saved\` before clearing the logs.

## Formatting & Linting
You don't have to do any of these things. They are just nice things to format the code and respect industry standards while checking for potential errors. They are not enforced with git hooks and "bad" code can still be pushed without shame ;-)

However, if you want to be a good contributor and commit pretty code, before committing run:
```bash
isort .
```
for sorting imports. And:
```bash
black .
```
for proper formatting.

If you also want to run some linters that check for potential issues in your code run:
```bash
pylint src
```
for static analysis (errors, warnings, and docstring). You should strive to get the best score you can.
```bash
flake8 src
```
for code style. If this doesn't output anything your code is very stylish!
```bash
mypy --ignore-missing-imports --install-types --non-interactive --package src
```
for type checking.