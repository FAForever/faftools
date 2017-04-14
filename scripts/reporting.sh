#!/bin/bash
# This script runs SQL selects inside the docker FAF db and copies them outside the container

IN_DOCKER="docker exec -i stable_faf-db_1  "

DATA_PATH="/opt/stable/content/reports"
WEB_PATH="/opt/stable/content"
FILE_NAME="reports.tar.xz"

# ** Setup all SQL queries
# add a new entry for each query you want to
# run key name will be used for filename
declare -A selects

#example queries
selects[game_stats]="SELECT * FROM game_stats;"
selects[game_player_stats]="SELECT * from game_player_stats;"

# Remove existing data
if [ -d "$DATA_PATH" ]
then
  rm -r "$DATA_PATH"
fi

mkdir "$DATA_PATH"

# Call all SQL statements and save them in ./data as $key.txt
for key in "${!selects[@]}"
do
    sql="${selects[$key]}"
    echo "Processing $key"
    echo "$sql"
    echo
    $IN_DOCKER mysql --login-path=faf_lobby faf_lobby -e "$sql" > "${DATA_PATH}/${key}.txt"
done

echo "Remove old file"
rm "${WEB_PATH}/${FILE_NAME}"

echo "Compressing all results"
tar -C $DATA_PATH -cJf "${WEB_PATH}/${FILE_NAME}" .

echo "Reports updated. Have a nice day."
