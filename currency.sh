#!/bin/bash
TERM=linux
export TERM
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"
NOCOLOR="$(tput sgr0)"

args=("$@")

truncate -s 0 ${args[1]}

filelength=$(wc -l ${args[0]} | awk '{ print $1 }') #How many lines exist in file.

prevclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.PrevClose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close
nowclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.

if [[ 10#09$nowclose -lt 10#09$prevclose ]] ; then #bearish
      high=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.High' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      prevclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Open' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      low=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      nowclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
      upwiq=$(expr \( $high - $prevclose \)) #today high - open
      downwiq=$(expr \( $nowclose - $low \)) #Calculate todaysclose -  low
      body=$(expr \( $prevclose - $nowclose \))
      time1=$((-10#09$time1))
      time1=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
      b="Bearish Candle"
      set -o errexit
       printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" >> ${args[1]}
      echo "${RED}Bearish${RED}${NOCOLOR} candle ${args[1]}"
      echo $time1
      nl=$'\n'
      echo "Nedkopt" ${RED}$upwiq${RED} ${NOCOLOR}
      echo "Uppkopt" ${GREEN}$downwiq${GREEN} ${NOCOLOR}
      echo "body"      ${RED}$body${RED} ${NOCOLOR}
      echo $nl
      sleep 1; bash -c "/root/currency/ifvalue15bear.sh ${args[1]} ${args[0]}"
      fi;

       filelength=$(wc -l ${args[0]} | awk '{ print $1 }') #How many lines exist in file.
       prevclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.PrevClose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close
       nowclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.
       
if [[ 10#09$nowclose -gt 10#09$prevclose ]] ; then  #if this close is higher than the previous close then we know that this is a bullish candle
       high=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.High' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
       low=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.
       nowclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #close under this hour.
       prevclose=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Open' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,5\}$/&0/;ta') #previous hourly close #previous hourly close
       upwiq=$(expr \( $prevclose - $low \)) #Calculate previous close - todays low
       downwiq=$(expr \( $high - $nowclose \)) #Calculate  today high - todays close
       body=$(expr \( $nowclose - $prevclose \))
       time1=$((-10#09$time1))
       time1=$(awk '{if(NR=='$filelength') print $0}' ${args[0]} | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
       b="Bullish Candle"
       set -o errexit
       printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" >> ${args[1]}
       echo "${GREEN}Bullish${GREEN}${NOCOLOR} Candle ${args[1]}"
       echo $time1
       nl=$'\n'
       echo "Nedkopt" ${RED}$downwiq${RED} ${NOCOLOR}
       echo "Uppkopt" ${GREEN}$upwiq${GREEN} ${NOCOLOR}
       echo "Body"    ${GREEN}$body${GREEN} ${NOCOLOR}
       echo $nl
       fi
