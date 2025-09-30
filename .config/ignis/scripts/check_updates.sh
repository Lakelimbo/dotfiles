#!/bin/bash

# obviously this is for Arch only

command="2>/dev/null | wc -l"
aur_command="yay -Qum $command"
official_command="checkupdates $command"

official_updates=$(eval "$official_command")
aur_updates=$(eval "$aur_command")

total_updates=$((official_updates + aur_updates))
echo $total_updates
