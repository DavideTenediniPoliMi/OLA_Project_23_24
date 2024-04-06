# OLA_Project_23_24

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