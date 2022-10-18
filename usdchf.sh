#!/bin/bash
TERM=linux
export TERM
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"
NOCOLOR="$(tput sgr0)"
#date1=$(date -d yesterday +%Y-%m-%d) #Yesterday
#date1=$(date +2022-05-09)
date1=$(date +%Y-%m-%d) #Today
#date2=$(date -d yesterday +%Y-%m-%d) #Yesterday
#date2="$(date -d @$time1)+2 hours"

truncate -s 0 /tmp/usdchf.txt;

file2=/tmp/usdchf1.txt
filelength=$(wc -l /tmp/usdchf1.txt | awk '{ print $1 }') #How many lines exist in file.

prevclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.PrevClose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close
nowclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.

if [[ 10#09$nowclose -lt 10#09$prevclose ]] ; then #bearish
      high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      prevclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      nowclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      upwiq=$(expr \( $high - $prevclose \)) #today high - open
      downwiq=$(expr \( $nowclose - $low \)) #Calculate todaysclose -  low
      body=$(expr \( $prevclose - $nowclose \))
      time1=$((-10#09$time1))
      time1=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
      b="Bearish Candle"
      set -o errexit
      file=/tmp/usdchf.txt
      exec 5>-
       printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" >> "$file";>&5
      exec 5>&-
      echo "${RED}Bearish${RED}${NOCOLOR} candle USDCHF"
      #e=$(date -d "$(LC_TIME=C date -d @$time1)+0 minute" +'%F %T' | cut -c -16)
      echo $time1
      nl=$'\n'
      echo "Nedkopt" ${RED}$upwiq${RED} ${NOCOLOR}
      echo "Uppkopt" ${GREEN}$downwiq${GREEN} ${NOCOLOR}
      echo "body"      ${RED}$body${RED} ${NOCOLOR}
      echo $nl
      sleep 1; bash -c "/files/ifvalueminute/usdchf/ifvalueminutebear.sh"
      fi;

       filelength=$(wc -l /tmp/usdchf1.txt | awk '{ print $1 }') #How many lines exist in file.
       prevclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.PrevClose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close
       nowclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.

if [[ 10#09$nowclose -gt 10#09$prevclose ]] ; then  #if this close is higher than the previous close then we know that this is a bullish candle
       high=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.High' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
       low=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.
       nowclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.
       #time1=$(awk '{if(NR==8) print $0}' /tmp/close/16x/gbpjpy.txt | cut -c -10)
       prevclose=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Open' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close #previous hourly close
       upwiq=$(expr \( $prevclose - $low \)) #Calculate previous close - todays low
       downwiq=$(expr \( $high - $nowclose \)) #Calculate  today high - todays close
       body=$(expr \( $nowclose - $prevclose \))
       time1=$((-10#09$time1))
       time1=$(awk '{if(NR=='$filelength') print $0}' $file2 | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
       b="Bullish Candle"
       set -o errexit
       file=/tmp/usdchf.txt
       exec 5>-
       printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" >> "$file";>&5
       exec 5>&-
       echo "${GREEN}Bullish${GREEN}${NOCOLOR} Candle USDCHF"
      #e=$(date -d "$(LC_TIME=C date -d @$time1)+0 minute" +'%F %T' | cut -c -16)
       #echo $e $time1
       echo $time1
       nl=$'\n'
       echo "Nedkopt" ${RED}$downwiq${RED} ${NOCOLOR}
       echo "Uppkopt" ${GREEN}$upwiq${GREEN} ${NOCOLOR}
       echo "Body"    ${GREEN}$body${GREEN} ${NOCOLOR}
       echo $nl
       #sleep 1; bash -c "/files/ifvalueminute/us30/BottomPattern/pattern1.sh"
