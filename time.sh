#!/bin/bash

year=$(date +%Y)
month=$(date +%m)
#month=$(date -d "2 month ago" +'%m')
minute="00"

sixteen="64"
holiday="66"

#When Pattern found 
startdate=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M") 

#When Pattern is created 
endate=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]} +$sixteen hour" +"%Y-%m-%d %H:%M") 

#Check time between those dates get unique value only business days 
abc=`python3 ./busyday.py "$startdate" "$endate" | sed 's/\..*$//'`

if [[ "$abc" -lt "$sixteen" ]]; then
   B=$(date -d "$(LC_TIME=C date -d "$startdate")+$holiday hour" +"%Y-%m-%d %H:%M") 
   D=`python ./compare.py "$endate" "$B" | sed 's/\..*$//'`
   val=$(expr \( $abc - $D \)) 
   value=$(expr \( $holiday - $abc \)) 
   convert=$(expr \( $value / 4 \)) 
   era=$(date -d "$(LC_TIME=C date -d "$B")+$value hour" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ') 
   echo "Weekend days!!"
   echo "Remaning candles after weekkend" $value
   echo "After Conversion" $convert
   echo "Final 16x pattern" $era
   echo "valuee is" $val
   echo "D is" $D
   echo "Start of Weekend B" $B
   python3 ./timer.py $era ${args[2]}   
else
   B=$(date -d "$(LC_TIME=C date -d "$startdate")+$sixteen hour" +"%Y-%m-%d %H:%M")
   value=$(expr \( $sixteen - $abc \)) 
   era=$(date -d "$(LC_TIME=C date -d "$B")+$value hour" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ') 
   echo "When Pattern was created" $startdate 
   echo "When Pattern is creating itself" $endate
   echo "Time Between startdate and weekend start is" $abc
   python3 ./timer.py $era ${args[2]}    
fi
