#!/bin/bash

screen="data"

cadjpy15=/root/tmp/cadjpy155.txt
result1=/root/tmp/cadjpy15.txt 
port1=9091

brent15=/root/tmp/brent155.txt
result2=/root/tmp/brent15.txt
port2=9093 

btcusd15=/root/tmp/btcusd155.txt
result3=/root/result/btcusd15.txt  
port3=2004

eurchf15=/root/tmp/eurchf155.txt 
result4=/root/tmp/eurchf15.txt 
port4=9099

eurusd15=/root/tmp/eurusd155.txt
result5=/root/tmp/eurusd15.txt 
port5=9098

gbpusd15=/root/tmp/gbpusd155.txt
result6=/root/tmp/gbpusd15.txt
port6=8086 

nas15=/root/tmp/nas10015.txt
result7=/root/tmp/nas100.txt
port8=7077

us15=/root/tmp/us155.txt
result8=/root/tmp/us15.txt
port9=8085 

usdcad15=/root/tmp/usdcad155.txt
result9=/root/tmp/usdcad15.txt 
port10=9097 

usdchf15=/root/tmp/usdchf155.txt
result10=/root/tmp/usdchf15.txt
port11=9096 

xauusd15=/root/tmp/xauusd155.txt
result11=/root/tmp/xauusd15.txt
port12=8082 

euraud15=/root/tmp/euraud155.txt
result12=/root/tmp/euraud15.txt
port13=9039 

currency=/root/tmp/currency.txt
port14=8087 

euraud4hour=/root/tmp/euraud4hour.txt
port15=9045

eurchf4hour=/root/tmp/euraud4hour.txt
port16=9046

eurusd4hour=/root/tmp/eurusd4hour.txt
port17=9047

tmux new -ds cadjpy15; tmux send-keys -t cadjpy15 'inotifywait -m -e close_write '$cadjpy15' --format --quiet | while read -r dir; do /root/currency/currency1.sh '$cadjpy15' '$result1'; done & ' Enter;

tmux new -ds brentcrude15; tmux send-keys -t brent15 'inotifywait -m -e close_write '$brent15' --format --quiet | while read -r dir; do /root/currency/currency2.sh '$brent15' '$result2'; done & ' Enter;

tmux new -ds btcusd15min; tmux send-keys -t btcusd15min 'inotifywait -m -e close_write '$cadjpy15' --format --quiet | while read -r dir; do /root/currency/currency3.sh '$btcusd15' '$result3'; done & ' Enter;

tmux new -ds eurchf15; tmux send-keys -t eurchf15 'inotifywait -m -e close_write '$eurchf15' --format --quiet | while read -r dir; do /root/currency/currency4.sh '$eurchf15' '$result4'; done &' Enter;

tmux new -ds eurusd15; tmux send-keys -t eurusd15 'inotifywait -m -e close_write '$eurusd15' --format --quiet | while read -r dir; do /root/currency/currency5.sh '$eurusd15' '$result5'; done &' Enter;

tmux new -ds gbpusd15min; tmux send-keys -t gbpusd15min 'inotifywait -m -e close_write '$gbpusd15' --format --quiet | while read -r dir; do /root/currency/currency6.sh '$gbpusd15' '$result6'; done &' Enter;

tmux new -ds nas10015; tmux send-keys -t nas10015 'inotifywait -m -e close_write '$nas15' --format --quiet | while read -r dir; do /root/currency/currency7.sh '$nas15' '$result7'; done &' Enter;

tmux new -ds us15; tmux send-keys -t us15 'inotifywait -m -e close_write '$us15' --format --quiet | while read -r dir; do /root/currency/currency8.sh '$us15' '$result8' ; done &' Enter;

tmux new -ds usdchf15; tmux send-keys -t usdchf15 'inotifywait -m -e close_write '$usdchf15' --format --quiet | while read -r dir; do /root/currency/currency9.sh '$usdchf15' '$result10'; done &' Enter;

tmux new -ds xauusd15; tmux send-keys -t xauusd15 'inotifywait -m -e close_write '$xauusd15' --format --quiet | while read -r dir; do /root/currency/currency10.sh '$xauusd15' '$result11'; done &' Enter;

tmux new -ds euraud15; tmux send-keys -t euraud15 'inotifywait -m -e close_write '$euraud15' --format --quiet | while read -r dir; do /root/currency/currency11.sh '$euraud15' '$result11'; done &' Enter

tmux new -ds euraud4hour; tmux send-keys -t euraud4hour 'inotifywait -m -e close_write '$euraud4hour' --format --quiet | while read -r dir; do /root/15min/euraud/euraud.sh; done &' Enter

tmux new -ds euraud4hour; tmux send-keys -t eurchf4hour 'inotifywait -m -e close_write '$eurchf4hour' --format --quiet | while read -r dir; do /root/15min/eurchf/eurchf.sh; done &' Enter

tmux new -ds usdcad15; tmux send-keys -t usdcad15 'inotifywait -m -e close_write '$usdcad15' --format --quiet | while read -r dir; do /root/currency/currency12.sh '$usdcad15' '$result9'; done &' Enter;


tmux new -ds ifvalues

tmux new -ds data
tmux new -ds telegrambot

sleep 2; 

adress=$(ip a | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')

tmux send-keys -t $screen python3' /root/server/serv1.py '$adress' '$port1' '$cadjpy15' &' Enter 

tmux send-keys -t $screen python3' /root/server/serv2.py '$adress' '$port2' '$brent15' &' Enter 

tmux send-keys -t $screen python3' /root/server/serv3.py '$adress' '$port3' '$btcusd15' &' Enter  

tmux send-keys -t $screen python3' /root/server/serv4.py '$adress' '$port4' '$eurchf15' &' Enter   

tmux send-keys -t $screen python3' /root/server/serv5.py '$adress' '$port5' '$eurusd15' &' Enter  

tmux send-keys -t $screen python3' /root/server/serv6.py '$adress' '$port6' '$gbpusd15' &' Enter

tmux send-keys -t $screen python3' /root/server/serv7.py '$adress' '$port7' '$ger15' &' Enter 

tmux send-keys -t $screen python3' /root/server/serv8.py '$adress' '$port8' '$nas15' &' Enter 

tmux send-keys -t $screen python3' /root/server/serv9.py '$adress' '$port9' '$us15' &' Enter
 
tmux send-keys -t $screen python3' /root/server/serv10.py '$adress' '$port10' '$usdcad15' &' Enter

tmux send-keys -t $screen python3' /root/server/serv11.py '$adress' '$port11' '$usdchf15' &' Enter

tmux send-keys -t $screen python3' /root/server/serv13.py '$adress' '$port12' '$xauusd15' &' Enter

tmux send-keys -t $screen python3' /root/server/serv12.py '$adress' '$port13' '$euraud15' &' Enter

tmux send-keys -t $screen python3' /root/server/serv14.py '$adress' '$port14' '$currency' &' Enter

tmux send-keys -t $screen python3' /root/server/serv15.py '$adress' '$port15' '$euraud4hour' &' Enter

tmux send-keys -t $screen python3' /root/server/serv16.py '$adress' '$port16' '$eurchf4hour' &' Enter

tmux send-keys -t $screen python3' /root/server/serv17.py '$adress' '$port17' '$eurusd4hour' &' Enter



