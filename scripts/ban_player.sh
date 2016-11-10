#!/bin/bash

read -p "User to ban: " user
read -p "Reason: " reason
read -p "Expires at: " expiry

echo "Banning user..."
docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "insert into lobby_ban (idUser, reason, expires_at) values ((select id from login where login = '${user}'), '${reason}', '${expiry}') on duplicate key update reason='${reason}', expires_at='${expiry}';"
echo "User banned."