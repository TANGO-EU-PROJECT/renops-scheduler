# renops-scheduler

**renops-scheduler** is a Python package that allows you to schedule and execute scripts at the time the most renewable energy is available.

This reduces the carbon footprint and stabilises the grid of our operations. In cases where the electricity price is variable, the scheduler also reduces utility costs. While its main focus are energy-intensive processing tasks such as big data analytics or AI model training, it may be used to shift any energy-intensive load such as HVAC.

## Requirements

Before you begin, ensure you have met the following requirements:

- **Python**: Version 3.8 or higher.

To check your Python version, run:

```bash
$ python3 --version
```

## Installation

To install **renops-scheduler**, run the following command:

```bash
$ pip install renops-scheduler
```

## Usage

Once you have installed **renops-scheduler**, you can use it to schedule and execute Python scripts in **command line interface (CLI)**.

To use the program, follow these steps:

1. Open a terminal or command prompt.
2. Create a new file named `test.py` containing:

    ```bash
    $ echo 'print("hello world!")' > test.py
    ```
3. Export `RENOPSAPI_KEY` env:

    ```bash
    $ export RENOPSAPI_KEY="TANGO_DEMO_KEY" 
    ```
    > **_NOTE:_** This is demo key with limited number of request. Contanct us to obtain personal access token. 
4. Run the following command to execute the script with a deadline of 24 hours:

    ```bash
    $ renops-scheduler test.py -la -r 6 -d 24 -v
    ```

    This will execute the `test.py` in an optimal window within the given deadline. 

    -  `-la` sets automatic location detection (uses machines public IP!),
    - `-r 6` sets runtime (estimated by user), 
    - `-d 24` sets the deadline to 24 hours. 

5. Scheduler can also find interval with minimal energy price:

    ```bash
    $ renops-scheduler test.py -la -r 6 -d 24 -v --optimise-price
    ```

    This is achieved by adding `--optimise-price` flag.

6. Running scheduler without automatic location detection:
    ```bash
    $ renops-scheduler test.py -l "Berlin,Germany" -r 6 -d 24 -v
    ```    
    In cases where a user **does not want to expose its IP**, due to privacy concerns, we can manually specify a rough location in a text description.

### Import Example
```python
from renops.scheduler import Scheduler

# Define a function with an argument that scheduler will execute
def test_run(a, text: str):
    print("Hello World!")
    print("Passed keyword argument:", text)
    print("Passed argument:", a)

# Intialise the scheduler
s = Scheduler(runtime=1,
              deadline=1,
              location="Kranj",
              verbose=True,
              optimise_price=True,
              action=test_run,
              argument=([42]),
              kwargs={"text": "Scheduler Test!"})

# Run the scheduler
s.run()
```

## Arguments
The program accepts several command-line arguments to customize the execution. Here's an overview of the available options:

```
usage: renops-scheduler [-h] -l LOCATION [-r RUNTIME] [-d DEADLINE] [-v VERBOSE] script_path

positional arguments:
  script_path           Path to the script to be executed.

options:
  -h, --help            show this help message and exit
  -l LOCATION, --location LOCATION
                        Location can be specified in two ways:
                        
                        1. Pass a specific location as a string, e.g., "Berlin, Germany".
                        
                        2. Use automatic location detection based on IP address.
                         By using this tag, you agree that your IP can be used to detect your location.
                        You can use any of the following values for this purpose:
                           -l a (-la)
                           -l auto
                           -l automatic
  -r RUNTIME, --runtime RUNTIME
                        Runtime in hours. (User estimated) - Deafult is 3 hours
  -d DEADLINE, --deadline DEADLINE
                        Deadline in hours, by when should script finish running - Default is 120 hours
  -op, --optimise-price
                        Optimise for energy price.
  -v, --verbose         Verbose mode.
```
## Privacy

The script does **not pose security or privacy concerns**, as it runs locally. The communication between our forecasting API is encrypted and includes an approximate location of the requested forecast. Automatic localization through IP is mandatory and must be manually set.
 
## Notes

- **renops-scheduler** is currently in beta version and may contain bugs or limitations.
- Send possible suggestions, bugs and improvements to ***jakob.jenko@xlab.si***
