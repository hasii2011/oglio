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

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"

python -m tests.TestAll
status=$?


echo "Exit with status: ${status}"
exit "${status}"
