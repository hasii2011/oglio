#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

echo "current: $(pwd)"

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --check-untyped-defs oglio tests
# mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --no-incremental oglio tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes oglio tests
status=$?

echo "Exit with status: ${status}"
exit ${status}
