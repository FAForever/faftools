#!/bin/bash

QUERY="SELECT l.id,l.login,l.password,l.email,l.ip,l.steamid,l.update_time,b.expires_at FROM login l left join ban b on (b.player_id = l.id) where l.email regexp '^[a-z]{3}[0-9]{5}@'order by l.update_time asc;"

echo "$QUERY"
docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "$QUERY" | tail -n 50
