#!/bin/bash

screen="data"

cadjpy15=/root/tmp/cadjpy155.txt
port1=9091

brent15=/root/tmp/brent155.txt
port2=9093 

btcusd15=/root/tmp/btcusd155.txt
port3=2004

eurchf15=/root/tmp/eurchf155.txt 
port4=9094 

eurusd15=/root/tmp/eurusd155.txt
port5=9098

gbpusd15=/root/tmp/gbpusd155.txt
port6=8086 

ger15=/root/tmp/ger155.txt
port7=8089 

nas15=/root/tmp/nas10015.txt
port8=7077

us15=/root/tmp/us155.txt
port9=8085 

usdcad15=/root/tmp/usdcad155.txt
port10=9097 

usdchf15=/root/tmp/usdchf155.txt
port11=9096 

xauusd15=/root/tmp/xauusd155.txt
port12=8082 

euraud15=/root/tmp/euraud155.txt
port13=9039 

currency=/root/tmp/currency.txt
port14=8087 

tmux new -ds cadjpy15min; tmux send-keys -t cadjpy15min 'inotifywait -m -e close_write "$cadjpy15" --format --quiet | while read -r dir; do /files/15min/cadjpy/cadjpy.sh; done & ' Enter;
tmux new -ds brentcrude15;
tmux new -ds btcusd15min; tmux send-keys -t btcusd15min 'inotifywait -m -e close_write "$btcusd15" --format --quiet | while read -r dir; do /files/15min/btcusd/btcusd.sh; done &' Enter;
tmux new -ds eurchf15; tmux send-keys -t eurchf15 'inotifywait -m -e close_write "$eurchf15" --format --quiet | while read -r dir; do /files/15min/eurchf/eurchf.sh; done &' Enter;
tmux new -ds eurusd15; tmux send-keys -t eurusd15 'inotifywait -m -e close_write "$eurusd15" --format --quiet | while read -r dir; do /files/15min/eurusd/eurusd.sh; done &' Enter;
tmux new -ds gbpusd15min; tmux send-keys -t gbpusd15min 'inotifywait -m -e close_write "$gbpusd15" --format --quiet | while read -r dir; do /files/15min/gbpusd/gbpusd.sh; done &' Enter;
tmux new -ds ger15; tmux send-keys -t ger15 'inotifywait -m -e close_write "$ger15" --format --quiet | while read -r dir; do /files/15min/ger/ger.sh; done &' Enter;
tmux new -ds nas10015; tmux send-keys -t nas10015 'inotifywait -m -e close_write "$nas15" --format --quiet | while read -r dir; do /files/15min/nas100/nas100.sh; done &' Enter;
tmux new -ds us15; tmux send-keys -t us15 'inotifywait -m -e close_write "$us15" --format --quiet | while read -r dir; do /files/15min/us30/us.sh; done &' Enter;
tmux new -ds usdcad15; tmux send-keys -t usdcad15 'inotifywait -m -e close_write "$usdcad15" --format --quiet | while read -r dir; do /files/15min/usdcad/usdcad.sh; done &' Enter;
tmux new -ds usdchf15; tmux send-keys -t usdchf15 'inotifywait -m -e close_write "$usdchf15" --format --quiet | while read -r dir; do /files/15min/usdchf/usdchf.sh; done &' Enter;
tmux new -ds xauusd15; tmux send-keys -t xauusd15 'inotifywait -m -e close_write "$xauusd15" --format --quiet | while read -r dir; do /files/15min/xauusd/xauusd.sh; done &' Enter;
tmux new -ds euraud15; tmux send-keys -t euraud15 'inotifywait -m -e close_write "$euraud15" --format --quiet | while read -r dir; do /files/15min/euraud/euraud.sh; done &' Enter
tmux new -ds ifvalues
tmux new -ds data
tmux new -ds telegrambot

sleep 2; 

adress=$(ip a | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')

tmux send-keys -t $screen python3' /root/server/serv1.py "$adress" '$port1' "$cadjpy15" &' Enter 

tmux send-keys -t $screen python3' /root/server/serv2.py "$adress" '$port2' "$brent15" &' Enter 

tmux send-keys -t $screen python3' /root/server/serv3.py "$adress" '$port3' "$btcusd15" &' Enter  

tmux send-keys -t $screen python3' /root/server/serv4.py "$adress" '$port4' "$eurchf15" &' Enter   

tmux send-keys -t $screen python3' /root/server/serv5.py "$adress" '$port5' "$eurusd15" &' Enter  

tmux send-keys -t $screen python3' /root/server/serv6.py "$adress" '$port6' "$gbpusd15" &' Enter

tmux send-keys -t $screen python3' /root/server/serv7.py "$adress" '$port7' "$ger15" &' Enter 

tmux send-keys -t $screen python3' /root/server/serv8.py "$adress" '$port8' "$nas15" &' Enter 

tmux send-keys -t $screen python3' /root/server/serv9.py "$adress" '$port9' "$us15" &' Enter
 
tmux send-keys -t $screen python3' /root/server/serv10.py "$adress" '$port10' "$usdcad15" &' Enter

tmux send-keys -t $screen python3' /root/server/serv11.py "$adress" '$port11' "$usdchf15" &' Enter

tmux send-keys -t $screen python3' /root/server/serv13.py "$adress" '$port12' "$xauusd15" &' Enter

tmux send-keys -t $screen python3' /root/server/serv14.py "$adress" '$port14' "$currency" &' Enter







