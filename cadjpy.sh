#!/bin/bash

image="/files/19x/cadjpy.png" #Image of Candlesticks
file2="/tmp/cadjpy155.txt" #Data Values
file3="/files/19x/cadjpy/15min.json" #Unsorted time of the day always the same numbers.
file4="/files/19x/cadjpy/15min2.json" #Sorted time of the day, depending on what the user types
file5="/files/19x/cadjpy/15min3.json"
x1="/files/19x/cadjpy/candlestick1.py" #Pattern1
x2="/files/19x/cadjpy/candlestick2.py" #Pattern2
x3="/files/19x/cadjpy/candlestick3.py" #Pattern3 

truncate -s 0 $file4;

echo "Enter Currency"
read sentiment

echo "Enter time"
read now

cap16="16x $sentiment"
cap19="19x $sentiment"
cap23="23x $sentiment"

echo $x
echo $xx
echo $xxx

if [[ -z $x ]] ; then #if 16x is empty
   a9=$(wc -l $file4 | awk '{ print $1 }') #print the containing lines
   var=$((16-$a9)) #Calculate how many lines is missing.
   t1=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   #t2=$(date +%Y-%m-%d-$t1)
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap16 "$t3"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x1 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap16 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=chatid'
   #gcalcli --calendar '15_min' add --title "16x $sentiment 15 min" --where "$now" --when "$t1" --duration 60 --description 'It is going to be hard!' --reminder 1 --who 'proactive1993@gmail.com'
else
   t6=$(awk '{if(NR==16) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   #t2=$(date +%Y%m%d$t6)
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR==16) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR==16) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap16 "$t3"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   Sec=$(($filelength))
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x1 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap16 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=chatid' > /dev/null
   fi;

if [[ -z $xx ]] ; then #if 19x is empty
   a9=$(wc -l $file4 | awk '{ print $1 }') #print the containing lines
   var=$((19-$a9)) #Calculate how many lines is missing.
   t1=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   #t2=$(date +%Y%m%d$t1)
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap19 "$t3"
   bash -c "/files/git/telegrambot.sh '19x $sentiment'"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   Sec=$(($filelength - 3))
   open1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x2 $open1 $close1 $high1 $low1 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap19 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=2012646742' > /dev/null
   #gcalcli --calendar '15_min' add --title "19x $sentiment 15 min" --where "$now" --when "$t1" --duration 60 --description 'It is going to be hard!' --reminder 1 --who 'proactive1993@gmail.com'
else
   t6=$(awk '{if(NR==19) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   #t2=$(date +%Y%m%d$t6)
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR==19) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR==19) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   ab="19x"
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap19 "$t3"
   bash -c "/files/git/telegrambot.sh '19x $sentiment'"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   Sec=$(($filelength - 3))
   open1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low1=$(awk '{if(NR=='$Sec') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x2 $open1 $close1 $high1 $low1 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap19 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=2012646742' > /dev/null
   fi

if [[ -z $xxx ]] ; then #if 22x is empty
   a9=$(wc -l $file4 | awk '{ print $1 }') #print the containing lines
   var=$((22-$a9)) #Calculate how many lines is missing.
   #t1=$(awk '{if(NR=='$var') print $0}' /files/15min3.json | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR=='$var') print $0}' $file5 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap23 "$t3"
   bash -c "/files/git/telegrambot.sh '23x $sentiment'"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   Two=$(($filelength - 3))
   Three=$(($filelength - 6))
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   open2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   open3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x3 $open3 $close3 $high3 $low3 $open2 $close2 $high2 $low2 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap23 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=2012646742' > /dev/null
else
   t6=$(awk '{if(NR==22) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta')
   year=$(date +%Y)
   month=$(date +%m)
   day=$(date +%d)
   hour=$(awk '{if(NR==22) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | cut -c -2)
   minute=$(awk '{if(NR==22) print $0}' $file4 | sed -e ':a;s/^.\{0,3\}$/0&/;ta' | tail -c 3)
   t2=$(date -d "$hour" +%Y-%m-%d" $hour:$minute")
   t3=$(date -d "$(LC_TIME=C date -d "$t2")+15 minute" +'%F %T' | cut -c -16)
   python3 /files/19x/timer.py $year $month $day $hour $minute $sentiment $cap23 "$t3"
   bash -c "/files/git/telegrambot.sh '23x $sentiment'"
   sleep 904
   filelength=$(wc -l $file2 | awk '{ print $1 }') #How many lines exist in file.
   Two=$(($filelength - 3))
   Three=$(($filelength - 6))
   open=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   open2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low2=$(awk '{if(NR=='$Two') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   open3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low3=$(awk '{if(NR=='$Three') print $0}' $file2 | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 $x3 $open3 $close3 $high3 $low3 $open2 $close2 $high2 $low2 $open $close $high $low $image
   curl -F "photo=@$image" -F "caption=$cap23 at $t2" 'https://api.telegram.org/botapikey/sendphoto?chat_id=2012646742' > /dev/null
   #echo "alert is set for" $t2
   #gcalcli --calendar '15_min' add --title "22x $sentiment 15 min" --where "$now" --when "$t2" --duration 60 --description 'It is going to be hard!' --reminder 1 --who 'proactive1993@gmail.com'
   fi


