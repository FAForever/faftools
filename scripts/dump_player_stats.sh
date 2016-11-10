#!/bin/bash

mkdir -p target
targetFile="target/game_and_player_stats.sql"

echo "Dumping data to ${targetFile}"
docker exec -i stable_faf-db_1 mysqldump --login-path=faf_lobby faf_lobby game_stats game_player_stats > ${targetFile}