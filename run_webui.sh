#!/bin/sh
#
# This script is run as root by supervisord. This wraps running the MineOS web
# server so that SIGTERM can be caught when the parent Docker container is
# stopped. Upon stop, any running Minecraft servers will be properly shutdown.
#
# Authors: Caleb P. Burns
# Created: 2021-09-29
# Updated: 2021-09-29
#

# Trap on SIGTERM to shutdown Minecraft servers.
trap 'sudo -u "$USER_NAME" /usr/games/minecraft/shutdown_servers.sh' SIGTERM

# Run webui.
/usr/games/minecraft/webui.js
