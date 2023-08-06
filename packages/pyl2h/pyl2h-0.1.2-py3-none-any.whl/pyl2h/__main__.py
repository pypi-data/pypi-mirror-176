import argparse
import asyncio
from time import sleep
from .udp import UDPServer

server = UDPServer()

def get_arguments() -> argparse.Namespace:
    """Get parsed passed in arguments."""

    parser = argparse.ArgumentParser(
        description="Matter Controller Server using WebSockets."
    )
    parser.add_argument(
        "--ip",
        type=str,
        default=None,
        help="IP of the device to be used for testing. Will Flip-Flop Channel 1 every Minute",
    )

    arguments = parser.parse_args()

    return arguments

def deviceCallback(deviceStatus):
    print("New Device Update: {}".format(deviceStatus))

def monitorUpdates():
    server.listen(deviceCallback)

def main() -> int:
    args = get_arguments()
    ip = args.ip

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, monitorUpdates)
    
    while True:
        devices = server.getDevices()
        print("Devices:")
        for d in devices:
            print(devices[d])

        if ip is not None and ip in devices:
            dev = devices[ip]
            newState = not dev["channels"][1]
            print("Switching device {} to {}".format(ip, newState))
            server.setStatus(ip, 1, newState)

        sleep(60)