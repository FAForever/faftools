#!/bin/bash

QUERY="SELECT l.email FROM login l where l.email regexp '^[a-z]{3}[0-9]{5}@';"

echo "$QUERY"
docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "$QUERY" | grep -o '@.*$' | sort | uniq -c | sort -g
