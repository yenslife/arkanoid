#!/bin/bash 

run_mlgame() {
    python -m mlgame -1 --nd -f 9000 -i ./ml/ml_play_collect.py . --difficulty NORMAL --level $1
}

for ((level=1; level<=25; level++))
do
    for ((i=1; i<=2; i++))
    do
        run_mlgame $level
    done
done
