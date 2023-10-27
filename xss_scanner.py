#!/usr/bin/python

#global imports
from datetime import datetime

#local imports
import scan
import info
import fuzz
import arguments
from termcolor import colored


user_input = arguments.get_arguments()

#User's input
type = user_input[0]
payload_codes = user_input[1]
fuzzing = user_input[2]
targets = user_input[3]
start_time = datetime.now()

try:
    for target in targets:
        print(colored(f"Scanning {target}", "blue"))
        try:
            if target[:4] != "http":
                protocol = info.check(target)
                if protocol:
                    target = f"{protocol}://{target}"
            else:
                if info.is_alive(target):
                    pass

        except Exception:
            print("Host is unreachable")

        # Get info about technologies used in website
        information = info.get_technologies(target)
        print(information[0])
        print(information[1]+"\n")

        if payload_codes and type:
            scanner = scan.Scanner(target, type, payload_codes)

            try:
                # Starting scanner
                scanner.crawl()
                scanner.run_scanner()
            except Exception:
                pass

        #doing fuzzing
        if fuzzing == "basic":
            fuzz.basic_fuzzing(target)
        elif fuzzing:
            fuzz.custom_fuzzing(target, fuzzing)
        print("\n" + "-" * 60 + "\n")

except KeyboardInterrupt:
    print(colored("\nExiting ...", "red"))
    exit()

# Duration of scan
end_time = datetime.now()
duration = info.get_time(end_time - start_time)

print(f"Done: {len(targets)} site(s) scanned in {duration} seconds")