#!/bin/bash

run_mlgame() {
    python -m mlgame -1 --nd -f 1000000 -i ./ml/ml_play_collect.py . --difficulty NORMAL --level $1
}

record_game() {
    python -m mlgame -1 -f 120 -i ./ml/ml_play_collect.py . --difficulty NORMAL --level $1
}

# for ((level=1; level<=9; level++))
# do
#     for ((i=1; i<=5; i++))
#     do
#         run_mlgame $level
#     done
# done

# for ((level=1; level<=9; level++))
# do
#     for ((i=1; i<=20; i++))
#     do
#         run_mlgame $level
#     done
# done

# for ((level=10; level<=23; level++))
# do
#     for ((i=1; i<=5; i++))
#     do
#         run_mlgame $level
#     done
# done

# for ((level=10; level<=23; level++))
# do
#     if [ $level -ne 10 ] && [ $level -ne 18 ] && [ $level -ne 19 ]; then
#         for ((i=1; i<=3; i++))
#         do
#             run_mlgame $level
#         done
#     fi
# done
#

for ((level=1; level<=23; level++))
do
    run_mlgame $level
done
