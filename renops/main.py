#!/usr/bin/env python3

import argparse
from argparse import RawTextHelpFormatter

from renops.scheduler import Scheduler, execute_script


def main():
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
    parser.add_argument("-v", "--verbose", type=bool, default=True, help="Verbose mode.")

    args = parser.parse_args()

    if not args.runtime:
        print("Runtime not specified, using default setting of 3 hours!")
        args.runtime = 3
    s = Scheduler(
        deadline=args.deadline,
        runtime=args.runtime,
        location=args.location,
        verbose=args.verbose,
        action=execute_script,
        argument=([args.script_path]),
    )
    s.run()


if __name__ == "__main__":
    main()
