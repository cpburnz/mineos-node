#!/bin/sh
#
# This script will safely shutdown all running Minecraft servers.
#
# Authors: Caleb P. Burns
# Created: 2021-09-29
# Updated: 2021-09-29
#

# This script must be run by the mc user, not root.
if [ "$(id -u)" -eq 0 ]; then
	echo 'This script must be run by the configured mc user, not root.'
	exit 1
fi

# Get server list.
server_list=$(ls -1 /var/games/minecraft/servers)

# Shutdown each server.
mineos_console=/usr/games/minecraft/mineos_console.js
echo "$server_list" | while IFS= read -r server; do
	echo "Shutdown $server"
	if $mineos_console -s "$server" -- verify up; then
		$mineos_console -s "$server" -- stop
		echo "Server $server shutdown complete."
	else
		echo "Server $server is already down."
	fi
done
