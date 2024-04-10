#!/usr/bin/env bash

while true; do
    read -p "ok to commit? [y/n]: " choice
    case $choice in
        [Yy]*) exit 0  ;;  
        [Nn]*) echo "Aborted" ; exit 1 ;;
    esac
done

exit 0
