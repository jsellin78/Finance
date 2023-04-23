#!/bin/bash

TERM=linux
export TERM
GREEN="$(tput setaf 2)"
YELLOW="$(tput setaf 3)"
NOCOLOR="$(tput sgr0)"



#echo "day and hour time"
#read sentiment

year=$(date +%Y)
month=$(date +%m)
#month=$(date -d "1 month ago" +'%m')
minute="00"
ninteen="72" 
sixteen="60"
noweekend="64"


args=("$@")
#echo $# arguments passed
#echo "$year"-"$month"-${args[0]} ${args[1]}":$minute" 
                  #day       #hour 

# HOW THE FORMAT LOOKS 
#startdate=$(date -d "1500 2023-04-17 +3 hours" +"%Y-%m-%d %H:%M")

#When Pattern found 
startdate=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")

form=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')

#IF THIS VALUE IS GREATER THAN FRIDAY THEN WE KNOW PATTERN CREATED OUTSIDE OF WEEKEND.   
endate=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]} +$sixteen hour" +"%Y-%m-%d %H:%M") 

echo "form is" $form
#friday=`python3 ./upcomingfriday.py $form` #prints the exact date of comming friday 

friday123=`python3 ./friday123.py $form` #prints the exact date of comming friday 
#fridayy=`python3 ./friday.py "$form" | tr ' ' '-' | '19:00'` #prints the exact date of comming friday 
VAL1=$(date +%s -d"$endate")
VAL2=$(date +%s -d"$friday123")

#echo "endate Pattern was created at" $endate
ted="19:00"

if [[ "$VAL1" > "$VAL2" ]]; then #if value is greater than friday close. Then we know that the pattern was created next week  
    echo "Pattern is greater than friday" #
    hours_inbetween=`python3 ./busyday.py "$startdate" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $sixteen - $hours_inbetween \))
    left_over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val hour" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "final 16x pattern after weekend is" ${YELLOW}$left_over${YELLOW} $NOCOLOR
    #B=$(date -d "$(LC_TIME=C date -d "$left_over")+$val hour" +"%Y-%m-%d %H:%M") 
    echo "Pattern was created at"${NOCOLOR} ${YELLOW}$startdate${YELLOW} $NOCOLOR
    echo "Sunday is" $sunday
    echo "Friday is" $friday123 # "friday is " $friday
    echo "hours from startdate to friday close" $hours_inbetween
    echo $val "Missing hours from sunday to next week"
    python3 ./timer.py $left_over ${args[2]}
    /root/newstart/candle.sh first '/root/tmp/${args[2]}4hour.txt'
    
else
    echo "startdate" $startdate
    left=$(date -d "$(LC_TIME=C date -d "$startdate")+$noweekend hour" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ') #first pattern 16x  
    python3 ./timer.py $left ${args[2]}
    echo "No weekend" $left 
fi
    
#When Pattern found 
startdate1=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")
form=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')
#IF THIS VALUE IS GREATER THAN FRIDAY THEN WE KNOW PATTERN CREATED OUTSIDE OF WEEKEND.   
endate1=$(date -d "${args[1]}$minute $year"-"$month"-"${args[0]} +$ninteen hour" +"%Y-%m-%d %H:%M") 

VAL3=$(date +%s -d"$endate1")
VAL4=$(date +%s -d"$friday123")

if [[ "$VAL3" > "$VAL4" ]]; then 
    echo "Pattern is greater than friday" #
    hours_inbetween=`python3 ./busyday.py "$startdate1" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $ninteen - $hours_inbetween \))
    over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val hour" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "final 19x pattern after weekend is" ${YELLOW}$_over${YELLOW} $NOCOLOR
    echo "Pattern was created at"${NOCOLOR} ${YELLOW}$startdate1${YELLOW} $NOCOLOR
    echo "Sunday is" $sunday
    echo "Friday is" $friday123 # "friday is " $friday
