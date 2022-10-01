time1=$(( 10#$time1 ))
    #2>&1 means that stderr is redirected to stdout
    #3>&- means that file descriptor 3, opened for writing(same as stdout), is closed.

#Strategy based on realtime processing of CandleSticks. 
#This is a Strategy based on Time and the width & height pattern of a candlestick. 
# It is discontinued.
# it provides a very powerful way to know where the direction of where the market is going. Especially if you have a system to do this on multiple CandleSticks. 
# I recommend you to be convervative about the values you put. And that you implement this on multiple candlesticks for best results. 

exec 4</tmp/eurusd.txt
IFS= read -ru4 body #Body
IFS= read -ru4 c #Uppköpt Candle green
IFS= read -ru4 d #Nedköpt Candle red
IFS= read -ru4 time1
exec 4<&-

if (( c >= 48 && c<= 53 && d >= 48 && d <= 53 && body >= 25 && body <= 30)); then
 echo "c and d is more than 48 but less than 53 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" > "/files/goodcandleseurusd.txt"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T') #16X
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T') #19X
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T') #22X
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 gcalcli --calendar '15_min' add --title "16x 15min eurusd" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x 15min eurusd" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x 15min eurusd" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 16 && c<= 20 && d >= 16 && d <= 20 && body >= 1 && body <= 1000)); then
 echo "c and d is more than 16 but less than 20 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 13 && c<= 16 && d >= 13 && d <= 16 && body >= 40 && body <= 50)); then
 echo "c and d is more than 13 but less than 16 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 10 && c<= 14 && d >= 10 && d <= 14 && body >= 17 && body <= 52)); then
 echo "c and d is more than 10 but less than 14 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 27 && c<= 32 && d >= 27 && d <= 32 && body >= 27 && body <= 32)); then
 echo "c and d is more than 27 but less than 32 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 19 && c<= 23 && d >= 19 && d <= 23 && body >= 45 && body <= 57)); then
 echo "c and d is more than 19 but less than 23 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 14 && c<= 16 && d >= 14 && d <= 16 && body >= 15 && body <= 20)); then
 echo "c and d is more than 14 but less than 16 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 14 && c<= 16 && d >= 14 && d <= 16 && body >= 15 && body <= 20)); then
 echo "c and d is more than 14 but less than 16 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 34 && c<= 44 && d >= 34 && d <= 44 && body >= 45 && body <= 50)); then
 echo "c and d is more than 34 but less than 44 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 22 && c<= 26 && d >= 22 && d <= 26 && body >= 65 && body <= 75)); then
 echo "c and d is more than 22 but less than 26 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 22 && c<= 26 && d >= 22 && d <= 26 && body >= 1 && body <= 65)); then
 echo "c and d is more than 22 but less than 26 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 6 && c<= 7 && d >= 6 && d <= 7 && body >= 7 && body <= 10)); then
 echo "c and d is more than 22 but less than 26 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 26 && c<= 30 && d >= 26 && d <= 30 && body >= 17 && body <= 25)); then
 echo "c and d is more than 26 but less than 25 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 7 && c<= 10 && d >= 7 && d <= 10 && body >= 15 && body <= 22)); then
 echo "c and d is more than 5 but less than 10 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 46 && c<= 47 && d >= 46 && d <= 47 && body >= 60 && body <= 70)); then
 echo "c and d is more than 46 but less than 47 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 25 && c<= 27 && d >= 25 && d <= 27 && body >= 15 && body <= 30)); then
 echo "c and d is more than 25 but less than 27 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 20 && c<= 22 && d >= 20 && d <= 22 && body >= 25 && body <= 35)); then
 echo "c and d is more than 25 but less than 27 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 27 && c<= 31 && d >= 27 && d <= 31 && body >= 4 && body <= 10)); then
 echo "c and d is more than 25 but less than 27 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 30 && c<= 35 && d >= 30 && d <= 35 && body >= 25 && body <= 35)); then
 echo "c and d is more than 30 but less than 35 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 33 && c<= 38 && d >= 33 && d <= 38 && body >= 4 && body <= 8)); then
 echo "c and d is more than 30 but less than 35 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 19 && c<= 23 && d >= 19 && d <= 23 && body >= 20 && body <= 40)); then
 echo "c and d is more than 19 but less than 23 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 30 && c<= 35 && d >= 30 && d <= 35 && body >= 2 && body <= 20)); then
 echo "c and d is more than 19 but less than 23 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 32 && c<= 36 && d >= 32 && d <= 36 && body >= 35 && body <= 45)); then
 echo "c and d is more than 19 but less than 23 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 45 && c<= 50 && d >= 45 && d <= 50 && body >= 0 && body <= 10)); then
 echo "c and d is more than 50 but less than 45 EURUSD" $time1
 printf "%s\n" "$body" "$c" "$d" "$time1" >> "/files/goodcandleseurusd.txt"
 nl=$'\n'
 bash -c "/files/telegrambot.sh 'Good Candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 time2=$(date -d "$(LC_TIME=C date -d "$time1")+240 minutes" +'%F %T')
 time3=$(date -d "$(LC_TIME=C date -d "$time1")+285 minutes" +'%F %T')
 time4=$(date -d "$(LC_TIME=C date -d "$time1")+330 minutes" +'%F %T')
 gcalcli --calendar '15_min' add --title "16x eurusd 15min" --where "$time1" --when "$time2" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "19x eurusd 15min" --where "$time1" --when "$time3" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 gcalcli --calendar '15_min' add --title "22x eurusd 15min" --where "$time1" --when "$time4" --duration 0 --description 'It is going to be hard!' --reminder 5 --who 'proactive1993@gmail.com'
 fi;

if (( c >= 0 && c<= 5 && d >= 115 && d <= 300 && body >= 1 && body <= 25)); then
 bash -c "/files/telegrambot.sh 'bullish 15min doji candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 fi;

if (( c >= 78 && c<= 4000 && d >= 0 && d <= 5 && body >= 70)); then
 bash -c "/files/telegrambot.sh 'Reversal usually negative 15min candle Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 fi;

if (( c >= 15 && c<= 4000 && d >= 0 && d <= 3 && body >= 20)); then
 bash -c "/files/telegrambot.sh 'Inverted hammer Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
 fi;

if (( c >= 0 && c<= 3 && d >= 15 && d <= 4000 && body >= 20)); then
 bash -c "/files/telegrambot.sh 'Inverted hammer! Created on eurusd at $time1 $nl upwiq $c $nl dwnwiq $d $nl body $body'"
fi;
