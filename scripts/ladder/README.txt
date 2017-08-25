# ladder pool tool

This directory contains a set of very hacky scripts intended to help with ladder pool maintenance.

## get_ladder_maps.sh

This is just a wrapper around the query

    select lm.id, lm.idmap, mv.filename from ladder_map as lm join map_version as mv on lm.idmap = mv.id;

It shows the current ladder maps with filename.

## find_maps.sh

Puts all arguments passed to a query searching for "filename LIKE '%$ARG%'" in the map_version table.

This lets you quickly find maps by filename.

## ladder_map_update.py

Finds maps to add or remove by filename and shows table updates and query to do updates.

Example usage:

    ./ladder_map_update.py "+land_wilderness_v3.v0001" "+crashing_waves.v0005" "-land wilderness V2" "-crashing_waves.v0004"

Use find_maps.sh to find/confirm filenames first.
