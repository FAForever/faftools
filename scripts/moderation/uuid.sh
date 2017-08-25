#!/bin/bash

#QUERY="SELECT l.id,l.login,l.password,l.email,l.update_time,b.expires_at FROM login l left join ban b on (b.player_id = l.id) where l.email regexp '^[a-z]{3}[0-9]{5}@'order by l.update_time asc;"
QUERY="select distinct l.login, l.email, l.update_time, ui.hash, b.expires_at  from uniqueid ui join unique_id_users uiu on (ui.hash = uiu.uniqueid_hash) join login l on (l.id = uiu.user_id) left join ban b on (b.player_id = l.id) where ui.uuid regexp '^[A-Z-]*$' and ui.mem_SerialNumber regexp '^[A-Z-]*$' order by l.update_time desc limit 100;"

echo "$QUERY"
docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "$QUERY"
