#!/bin/bash

docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e "select lm.id, lm.idmap, mv.filename from ladder_map as lm join map_version as mv on lm.idmap = mv.id;"
