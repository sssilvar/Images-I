#!/bin/env bash

# Check if a string in a substring
FILE_PATH='/tmp/test/file.csv'
if [[ ${FILE_PATH} == *"file.csv" ]]; then
    echo "Has test.csv"
    FILE_PATH=$(dirname ${FILE_PATH})
    echo ${FILE_PATH}
fi