#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------

import argparse
import json

from pyduro.actions import ACTIONS, FUNCTIONS, discover, get, set

# -----------------------------------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        prog="PyDuro",
        description="Discover, query or modify an Aduro wood/pellet burner using the NBE communication protocol",
    )
    parser.add_argument(
        "-b",
        "--burner",
        help="The IP address of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "-s",
        "--serial",
        help="The serial number of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--pin",
        help="The pin code of the burner you want to query/modify",
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Display the raw frames sent and received",
        action="store_true",
    )
    parser.add_argument(
        "action",
        help='Run the given action (Default = "discover")',
        type=str,
        choices=ACTIONS,
        nargs="?",
        default=ACTIONS[0],
    )
    parser.add_argument(
        "function",
        help="Specify the part of the burner you want to query/modify",
        type=str,
        choices=FUNCTIONS,
        nargs="?",
    )
    parser.add_argument(
        "path",
        help="The path for your query/modification",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "value",
        help="The payload for your modification",
        type=str,
        nargs="?",
    )

    args = parser.parse_args()

    response = None
    if args.action == "discover":
        response = discover.run(verbose=args.verbose)
    elif args.action == "get":
        response = get.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            function_name=args.function,
            path=args.path,
            verbose=args.verbose,
        )
    elif args.action == "set":
        response = set.run(
            burner_address=args.burner,
            serial=args.serial,
            pin_code=args.pin,
            path=args.path,
            value=args.value,
            verbose=args.verbose,
        )

    if response:
        if args.action == "get":
            print(json.dumps(response.parse_payload(), sort_keys=True, indent=2))
        else:
            print(response.parse_payload())

        exit(response.status)

    exit(1)


# -----------------------------------------------------------------------------------------------------------------------

main()
