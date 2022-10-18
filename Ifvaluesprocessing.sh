#!/bin/bash

time1=$(( 10#$time1 ))
    #2>&1 means that stderr is redirected to stdout
    #3>&- means that file descriptor 3, opened for writing(same as stdout), is closed.

exec 4</tmp/us30.txt
IFS= read -ru4 body #body
IFS= read -ru4 c #high green #Nedkopt
IFS= read -ru4 d #low red #Uppkopt
IFS= read -ru4 time1
IFS= read -ru4 b #Bearish or Bullish
exec 4<&-

if (( c >= 0 && c<= 3 && d >= 13 && d <= 30 && body >= 13 && body <= 30)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 1, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 1. Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 3 && d >= 5 && d <= 7 && body >= 18 && body <= 24)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 2, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 2. created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 6 && d >= 4 && d <= 6 && body >= 25 && body <= 30)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 3, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 3. Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 18 && d <= 20 && body >= 18 && body <= 20)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 4, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 4. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 30 && d <= 35 && body >= 3 && body <= 6)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 5, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 5. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 0 && d <= 10 && body >= 3 && body <= 6)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 6, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 6. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 0 && d <= 30 && body >= 8 && body <= 25)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 7, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 7. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 3 && d >= 0 && d <= 4 && body >= 15 && body <= 19)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 8, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 8. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 5 && c<= 9 && d >= 10 && d <= 15 && body >= 20 && body <= 30)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 9, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 9. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 3 && d >= 10 && d <= 20 && body >= 15 && body <= 30)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 10, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 10. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 8 && d <= 20 && body >= 7 && body <= 15)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 11, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 11. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 8 && d <= 20 && body >= 7 && body <= 15)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 12, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 12. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 5 && d <= 20 && body >= 7 && body <= 15)) && [[ b == "Bullish Candle" ]]; then
 nl=$'\n'
 tmux send-keys -t ifvalues $"printf '\033[A\33[2K\r\e[32m%s\e[0m\n' 'Pattern 13, Matched djia30 at $time1'" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 13. Candle Created on us30 at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"
 fi


# \033[A makes printf go up a line (to the line showing the input command)
# \33[2K deletes the currnt line
# \r moves the cursor to the start of the current line
# %s prints the specified characters
# \n moves to the next line (otherwise the data would be at the start of the next command prompt line in ther terminal)



