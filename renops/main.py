#!/usr/bin/env python3

import argparse
import sys
from argparse import RawTextHelpFormatter

from renops.scheduler import Scheduler, execute_script


def main():
    try:
        run()

    except ValueError as error:
        print(f"ValueError: {error}")
        sys.exit(1)  # Exiting with status code 1 signifies an error

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting.")
        sys.exit(0)  # Exiting with status code 0 signifies a clean exit

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)  # Exiting with status code 1 for error


def run():
    print("RUNNING RENOPS SCHEDULER...")
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("script_path", help="Path to the script to be executed.")
    parser.add_argument(
        "-l",
        "--location",
        default=None,
        help=(
            "Location can be specified in two ways:\n\n"
            '1. Pass a specific location as a string, e.g., "Berlin, Germany".\n\n'
            "2. Use automatic location detection based on IP address.\n"
            " By using this tag, you agree that your IP can be used to detect your location.\n"
            "You can use any of the following values for this purpose:\n"
            "   -l a (-la)\n"
            "   -l auto\n"
            "   -l automatic\n"
        ),
        required=True,
    )
    parser.add_argument("-r", "--runtime", type=int, default=None, help="Runtime in hours.")
    parser.add_argument(
        "-d",
        "--deadline",
        type=int,
        default=120,
        help="Deadline in hours, by when should script finish running",
    )
    parser.add_argument("-op", "--optimise-price", action="store_true", help="Optimise for energy price.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode.")

    args = parser.parse_args()

    if args.optimise_price:
        print("Optimising for price! (Day-ahead forecast only)")

    if not args.runtime:
        print("Runtime not specified, using default setting of 3 hours!")
        args.runtime = 3

    s = Scheduler(
        deadline=args.deadline,
        runtime=args.runtime,
        location=args.location,
        optimise_price=args.optimise_price,
        verbose=args.verbose,
        action=execute_script,
        argument=([args.script_path]),
    )
    s.run()


if __name__ == "__main__":
    main()
