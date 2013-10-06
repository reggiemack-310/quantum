#!/bin/bash

COMMAND="clear & nosetests tests/$1.py --rednose -s"
echo $COMMAND

watchmedo shell-command \
    --patterns="*.py;*.txt" \
    --recursive \
    --command="$COMMAND" \
    .