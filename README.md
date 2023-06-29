# renops-scheduler

**renops-scheduler** is a Python package that allows you to schedule and execute Python scripts at time when most renewable energy available. This README provides instructions on how to use the program effectively.

## Installation

To install **renops-scheduler**, follow these steps:

1. Ensure that you have **pip** installed on your system.
2. Download the provided package distribution file `renops_scheduler-0.0.1.tar.gz`.
3. Open a terminal or command prompt and navigate to the directory where the file is located.
4. Run the following command to install the package:

   ```
   pip install renops_scheduler-0.0.1.tar.gz
   ```

## Usage

Once you have installed **renops-scheduler**, you can use it to schedule and execute Python scripts.

To use the program, follow these steps:

1. Open a terminal or command prompt.
2. Create a new file named `test.py` and write the following content to it:

   ```python
   print("Hello World!")
   ```

   Save the file in a directory of your choice.

3. Run the following command to execute the script with a deadline of 10 hours:

   ```
   renops-scheduler test.py -d 10
   ```

   This will execute the `test.py` script and find optimal execution window whitin given deadline.


## Optional arguments

The program accepts several command-line arguments to customize the execution. Here's an overview of the available options:
- `-l LOCATION`, `--location LOCATION`: Specify a location in the format "settlement,country" (e.g., "Berlin, Germany"). If not provided, scheduler automatically detects location based of the IP - (This will be optiononal in future releases)
- `-r RUNTIME`, `--runtime RUNTIME`: Specify the estimated runtime of given script in hours. The default value is 3 hours.
- `-d DEADLINE`, `--deadline DEADLINE`: Specify the deadline in hours, by when should the given script be executed. The default value is 120. If deadline is smaller than first feasible interval, the program will execute immediately.

## Notes

- **renops-scheduler** is currently in beta version and may contain bugs or limitations.
- Currently we select the most optimal interval based on limitations, so given script will always execute on full hour
- The program supports running Python scripts only.
- Send possible suggestions, bugs and improvements to ***jakob.jenko@xlab.si***
