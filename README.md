# renops-scheduler

**renops-scheduler** is a Python package that allows you to schedule and execute Python scripts with various options. This README provides instructions on how to use the program effectively.

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

3. Run the following command to execute the script immediately with a deadline of 1 hour:

   ```
   renops-scheduler test.py -d 1
   ```

   This will execute the `test.py` script with a deadline of 1 hour.

## Optional arguments
The program accepts several command-line arguments to customize the execution. Here's an overview of the available options:

The following options are available when using **renops-scheduler**:
- `-l LOCATION`, `--location LOCATION`: Specify a location in the format "settlement,country" (e.g., "Berlin, Germany"). If not provided, scheduler automatically detects location based of the IP!. (will be optional in future)
- `-r RUNTIME`, `--runtime RUNTIME`: Specify the runtime in hours. The default value is 3.
- `-d DEADLINE`, `--deadline DEADLINE`: Specify the deadline in hours. The default value is 120. If deadline is smaller than first feasible interval, the program will execute immediately

## Notes

- **renops-scheduler** is currently in beta version and may contain bugs or limitations.
- The program supports running Python scripts only.

Please note that this README provides a basic overview of how to use **renops-scheduler**. For more detailed instructions or specific usage examples contact jakob.jenko@xlab.si
