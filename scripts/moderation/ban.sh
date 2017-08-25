#!/bin/bash

PLAYER=$1
AUTHOR=$2
REASON=$3
TMS=$4

QUERY="insert into ban (player_id, author_id, reason, expires_at, level) select (select id from login where login='$PLAYER'), (select id from login where login='$AUTHOR'), '$REASON',  DATE_ADD(NOW(), INTERVAL $TMS), 'GLOBAL';"

echo "$QUERY"
docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "$QUERY"
