#!/bin/bash
TERM=linux
export TERM
GREEN="$(tput setaf 2)"
RED="$(tput setaf 1)"
NOCOLOR="$(tput sgr0)"

args=("$@")

#truncate -s 0 ${args[1]}

padd=6 #if last digit of string is missing padd it with a zero 
limit=6 #remove any extra digit if number is more than limit number we dont care about extra decimals   


prevclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].prevclose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
nowclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')

if [[ 10#09$nowclose -lt 10#09$prevclose ]] ; then #bearish
      high=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].high' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
      prevclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].prevclose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
      low=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
      nowclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
      upwiq=$(expr \( $high - $prevclose \)) #today high - open
      downwiq=$(expr \( $nowclose - $low \)) #Calculate todaysclose -  low
      body=$(expr \( $prevclose - $nowclose \))
      echo $high1 $low1 $open1 $close1 
      time1=$((-10#09$time1))
      time1=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].time')
      b="Bearish Candle"
      set -o errexit
       jq --argjson new_entry "{\"Currency\":\"${args[0]}\",\"Time\":\"$time1\",\"PrevClose\":$prevclose,\"Close\":$nowclose,\"High\":$high,\"Low\":$low,\"nedkopt\":$upwiq,\"upkopt\":$downwiq,\"body\":$body, \"b\":\"$b\"}"\
       '. as $array | [$new_entry] + $array | .[]' /root/tmp/4hr/"${args[0]}" | jq -s '.' | sponge /root/tmp/4hr/"${args[0]}"
      echo "${RED}Bearish${RED}${NOCOLOR} candle ${args[0]} "
      echo $time1 
      nl=$'\n'
      echo "Nedkopt" ${RED}$upwiq${RED} ${NOCOLOR}
      echo "Uppkopt" ${GREEN}$downwiq${GREEN} ${NOCOLOR}
      echo "body"      ${RED}$body${RED} ${NOCOLOR}
      echo $nl
      sleep 1; bash -c "/root/ifvalue/currency/4hr/ifval.sh ${args[0]} $time1"
      fi;


prevclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].prevclose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
nowclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')

if [[ 10#09$nowclose -gt 10#09$prevclose ]] ; then  #if this close is higher than the previous close then we know that this is a bullish candle       
       high=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].high' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
       prevclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].prevclose' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
       low=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].low' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
       nowclose=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].close' | awk '{gsub(/["".]/,""); print;}' | sed -e ':a;s/^.\{0,'$padd'\}$/&0/;ta' -e 's/^\([0-9]\{1,'$limit'\}\).*$/\1/')
       upwiq=$(expr \( $prevclose - $low \)) #Calculate previous close - todays low
       downwiq=$(expr \( $high - $nowclose \)) #Calculate  today high - todays close
       body=$(expr \( $nowclose - $prevclose \))
       time1=$((-10#09$time1))
       time1=$(curl -s http://192.168.1.220:2066/4hour/"${args[0]}" | jq -r '.[].time')
       b="Bullish Candle"
       set -o errexit 
       jq --argjson new_entry "{\"Currency\":\"${args[0]}\",\"Time\":\"$time1\",\"PrevClose\":$prevclose,\"Close\":$nowclose,\"High\":$high,\"Low\":$low,\"nedkopt\":$upwiq,\"upkopt\":$downwiq,\"body\":$body, \"b\":\"$b\"}"\
       '. as $array | [$new_entry] + $array | .[]' /root/tmp/4hr/"${args[0]}" | jq -s '.' | sponge /root/tmp/"${args[0]}"
       echo "${GREEN}Bullish${GREEN}${NOCOLOR} Candle ${args[0]}"
       echo $time1
       nl=$'\n'
       echo "Nedkopt" ${RED}$downwiq${RED} ${NOCOLOR}
       echo "Uppkopt" ${GREEN}$upwiq${GREEN} ${NOCOLOR}
       echo "Body"    ${GREEN}$body${GREEN} ${NOCOLOR}
       echo $nl
       sleep 1; bash -c "/root/ifvalue/currency/4hr/ifval.sh ${args[0]} $time1"
       fi;
