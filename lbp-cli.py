from lbp import littleblackpill
import argparse

parser = argparse.ArgumentParser(description='Run some LBP commands directly on the CLI.')

parser.add_argument('--action', help='What action to play.', required=True)
parser.add_argument('--device', help='Which device to target', required=True)
parser.add_argument('--qty', help="How many times should the action get played?")


args = parser.parse_args()

lbp = littleblackpill()
lbp.perform_action_on_device(args.device, args.action, args.qty)