#!/usr/bin/env python3
"""
This script is run as root by supervisord. This wraps running the MineOS web
server so that SIGTERM can be caught when the parent Docker container is
stopped. Upon stop, any running Minecraft servers will be properly shutdown.
"""

__authors__ = ["Caleb P. Burns"]
__created__ = "2021-09-29"
__updated__ = "2021-10-01"

import argparse
import os
import signal
import subprocess
from typing import List


def on_sigterm(signum: int, frame) -> None:
	"""
	Called when a SIGTERM is occurs.
	"""
	subprocess.run(["sudo", "-u", os.environ['USER_NAME'], "/usr/games/minecraft/shutdown_servers.sh"])


def main(argv: List[str]) -> int:
	"""
	Runs the script.
	"""
	# Parse command-line arguments.	
	parser = argparse.ArgumentParser(prog=argv[0], description=__doc__)
	parser.parse_args(argv[1:])

	# This script must be run by the root user.
	assert os.getuid() == 0, "This script must be run by root."
	assert os.environ.get('USER_NAME'), (
		f"The environment variable USER_NAME={os.environ.get('USER_NAME')} must be set."
	)

	# Setup SIGTERM handler.
	signal.signal(signal.SIGTERM, on_sigterm)

	# Run webui.
	subprocess.run(["/usr/games/minecraft/webui.js"], check=True)

	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))
