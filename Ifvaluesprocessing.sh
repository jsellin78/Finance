#!/bin/bash

time1=$(( 10#$time1 ))
    #2>&1 means that stderr is redirected to stdout
    #3>&- means that file descriptor 3, opened for writing(same as stdout), is closed.

exec 4</tmp/us30.txt
IFS= read -ru4 body #body
IFS= read -ru4 c #high green #uppkopt
IFS= read -ru4 d #low red #nedkopt
IFS= read -ru4 time1
exec 4<&-

if (( c >= 0 && c<= 3 && d >= 13 && d <= 30 && body >= 13 && body <= 30)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 1, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 1. Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 3 && d >= 5 && d <= 7 && body >= 18 && body <= 24)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 2, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 2. created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 6 && d >= 4 && d <= 6 && body >= 25 && body <= 30)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 3, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 3. Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 18 && d <= 20 && body >= 18 && body <= 20)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 4, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 4. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 30 && d <= 35 && body >= 3 && body <= 6)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 5, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 5. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 0 && d <= 10 && body >= 3 && body <= 6)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 6, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 6. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 0 && d <= 30 && body >= 8 && body <= 25)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "printf '\033[A\33[2K\r%s\n' 'Pattern Candle 7, Confirmed Created US30 on $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 7. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"
 fi;


# \033[A makes printf go up a line (to the line showing the input command)
# \33[2K deletes the currnt line
# \r moves the cursor to the start of the current line
# %s prints the specified characters
# \n moves to the next line (otherwise the data would be at the start of the next command prompt line in ther terminal)



