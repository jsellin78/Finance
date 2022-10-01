#!/bin/bash
TERM=linux
export TERM
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"
NOCOLOR="$(tput sgr0)"
date1=$(date +%Y-%m-%d) #Today

filelength=$(wc -l /tmp/btcusd_min.txt | awk '{ print $1 }') #Take The last line in file.
prevclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.PrevClose' | cut -c -5) #previous bar close
nowclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Close' | cut -c -5) #this bar close.

if [[ (($nowclose -lt $prevclose)) ]] ; then #Then we know this is a bearish Candle
      high=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.High' | cut -c -5)
      prevclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Open' | cut -c -5) #previous bar close
      low=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Low' | cut -c -5) #Low of candle
      nowclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Close' | cut -c -5) #this bar close.
      upwiq=$(expr \( $high - $prevclose \)) #high - open
      downwiq=$(expr \( $nowclose - $low \)) #close -  low
      body=$(expr \( $prevclose - $nowclose \))
      time1=$((-10#09$time1))
      time1=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
      b="Bearish Candle"
      set -o errexit
      file=/tmp/btcusd.txt
      exec 5>-
       printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" > "$file";>&5 #Print result to file for further processing.
      exec 5>&-
      echo "${RED}Bearish${RED}${NOCOLOR} candle BTCUSD"
      echo $time1
      nl=$'\n'
      echo "Nedkopt" ${RED}$upwiq${RED} ${NOCOLOR}
      echo "Uppkopt" ${GREEN}$downwiq${GREEN} ${NOCOLOR}
      echo "body"      ${RED}$body${RED} ${NOCOLOR}
      echo $nl
      fi;

       filelength=$(wc -l /tmp/btcusd_min.txt | awk '{ print $1 }') #Take The last line in file
       prevclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.PrevClose' | cut -c -5) #previous bar close
       nowclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Close' | cut -c -5) #this bar close

  if [[ $nowclose -gt $prevclose ]] ; then  #if this close is higher than the previous close then we know that this is a bullish candle
        high=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.High' | cut -c -5)
        low=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Low' | cut -c -5) #Low of candle
        nowclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Close' | cut -c -5) #this bar close.
        #time1=$(awk '{if(NR==8) print $0}' /tmp/close/16x/gbpjpy.txt | cut -c -10)
        prevclose=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Open' | cut -c -5) #previous close
        upwiq=$(expr \( $prevclose - $low \)) #previous close - bar low
        downwiq=$(expr \( $high - $nowclose \)) #high - close
        body=$(expr \( $nowclose - $prevclose \))
        time1=$((-10#09$time1))
        time1=$(awk '{if(NR=='$filelength') print $0}' /tmp/btcusd_min.txt | jq '.Time' | awk '{gsub(/["".]/,""); print;}')
        b="Bullish Candle"
        set -o errexit
        file=/tmp/btcusd.txt
        exec 5>-
        printf "%s\n" "$body" "$upwiq" "$downwiq" "$time1" "$b" > "$file";>&5 #Print result to file for further processing
        exec 5>&-
        echo "${GREEN}Bullish${GREEN}${NOCOLOR} Candle BTCUSD"
        #e=$(date -d "$(LC_TIME=C date -d @$time1)+0 minute" +'%F %T' | cut -c -16)
        #echo $e $time1
        echo $time1
        nl=$'\n'
        echo "Nedkopt" ${RED}$downwiq${RED} ${NOCOLOR}
        echo "Uppkopt" ${GREEN}$upwiq${GREEN} ${NOCOLOR}
        echo "Body"    ${GREEN}$body${GREEN} ${NOCOLOR}
        echo $nl
        fi;
