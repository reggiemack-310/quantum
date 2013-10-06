watchmedo shell-command \
    --patterns="*.py;*.txt" \
    --recursive \
    --command='clear & nosetests simulator_test.py --rednose -s' \
    .
