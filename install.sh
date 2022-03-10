#!/usr/bin/env bash

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Successfully installed Python packages"
else
    echo "Some error occurred. Please check you have Python 3 and pip installed"
fi