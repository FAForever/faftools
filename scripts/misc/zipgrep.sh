#!/bin/bash

TERM="$1"
shift

while (( "$#" )); do

    if ( unzip -l "$1" | grep -q "$TERM"); then
        echo "$1"
    fi

    shift
done
