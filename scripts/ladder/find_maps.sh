#!/bin/bash

QUERY="select id, filename from map_version where "

for arg in "$@"
do
  QUERY="$QUERY filename like '%$arg%' or"
done

QUERY="$QUERY 0=1;"

echo $QUERY

docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "$QUERY"
