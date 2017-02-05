import time
import argparse
import pyfldigi

parser = argparse.ArgumentParser(description='FLDIGI XML config file monitor + Logger')
parser.add_argument('-t', dest='timeout', nargs=1, type=float, default=[60.0], help='Timeout')
args = parser.parse_args()
timeout = args.timeout[0]
client = pyfldigi.Client()
m = pyfldigi.XmlMonitor(config_dir=client.config_dir)
time.sleep(timeout)
m.stop()
