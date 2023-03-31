#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

changeToProjectRoot

python3 -Wdefault -m tests.TestAll
status=$?


echo "Exit with status: ${status}"
exit "${status}"

