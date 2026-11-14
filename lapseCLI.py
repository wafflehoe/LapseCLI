import argparse
import httpx

parser = argparse.ArgumentParser(description="Interact with Lapse without Lookout.")

# TODO: add arguments
parser.add_argument("--api-key", type="str", help="")

args = parser.parse_args()

if args.run:
    print("uwu")