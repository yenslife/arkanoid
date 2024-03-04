#!/bin/bash

run_mlgame() {
    python -m mlgame -1 --nd -f 1000000 -i ./ml/ml_play_collect.py . --difficulty NORMAL --level $1
}

for ((level=1; level<=5; level++))
do
    for ((i=1; i<=50; i++))
    do
        run_mlgame $level
    done
done

# for ((level=1; level<=9; level++))
# do
#     for ((i=1; i<=20; i++))
#     do
#         run_mlgame $level
#     done
# done

for ((level=10; level<=23; level++))
do
    for ((i=1; i<=5; i++))
    do
        run_mlgame $level
    done
done
