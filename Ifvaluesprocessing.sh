#!/bin/bash

time1=$(( 10#$time1 ))
    #2>&1 means that stderr is redirected to stdout
    #3>&- means that file descriptor 3, opened for writing(same as stdout), is closed.

exec 4</tmp/btcusd.txt
IFS= read -ru4 body #body
IFS= read -ru4 c #high green #Nedköpt
IFS= read -ru4 d #low red #Uppköpt
IFS= read -ru4 time1
exec 4<&-

if (( c >= 0 && c<= 3 && d >= 13 && d <= 30 && body >= 13 && body <= 30)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 1 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 1. Created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 3 && d >= 5 && d <= 7 && body >= 18 && body <= 24)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 2 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 2. created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 6 && d >= 4 && d <= 6 && body >= 25 && body <= 30)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 3 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 3. Created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 18 && d <= 20 && body >= 18 && body <= 20)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 4 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 4. Candle Created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 30 && d <= 35 && body >= 3 && body <= 6)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 5 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 5. Candle Created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"

elif (( c >= 0 && c<= 4 && d >= 7 && d <= 30 && body >= 10 && body <= 25)); then
 nl=$'\n'
 tmux send-keys -t ifvalues "#Pattern Confirmed, Created 6 btcusd on $time1" Enter
 bash -c "/files/telegrambot.sh 'timeframe minute, Pattern we are looking for 7. Candle Created on btcusd at $time1 $nl Nedkopt $c $nl Uppkopt $d $nl body $body'"
 fi;
