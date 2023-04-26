#!/bin/bash
p="n43.png" 
sixteen="240"
ninteen="285"
twentiethree="330"
ted="19:00"
year=$(date +%Y)
month=$(date +%m)
currency1="16x 15 min ${args[3]}"
currency2="19x 15 min ${args[3]}"
currency3="22x 15 min ${args[3]}"

args=("$@")


                       #hour       #minute                      #day  #args[3] equals the currency provided you want to monitor 
startdate=$(date -d "${args[1]}":"${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")
form=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')
endate=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]} +$sixteen minutes" +"%Y-%m-%d %H:%M")
friday123=`python3 ./friday123.py $form` 

VAL1=$(date +%s -d"$endate")
VAL2=$(date +%s -d"$friday123")

if [[ "$VAL1" > "$VAL2" ]]; then 
    hours_inbetween=`python3 ./busyday.py "$startdate" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $sixteen - $hours_inbetween \))
    left_over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    python3 ./timer.py $left_over ${args[3]} "$currency1" "$startdate" "$left_over"
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') 
    open=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick1.py $open $close $high $low $p
    sleep 1  
    curl -F "photo=@$p" -F "caption=$currency1" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
else
   left=$(date -d "$(LC_TIME=C date -d "$startdate")+$sixteen minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')   
   python3 ./timer.py $left ${args[3]} "$currency2" "$startdate" "$left"
   sleep 904 
   filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') 
   open=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   close=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   high=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   low=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
   python3 ./candlestick1.py $open $close $high $low $p
   sleep 1 
   curl -F "photo=@$p" -F "caption=$des1" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
   fi;


startdate1=$(date -d "${args[1]}":"${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")
form=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')
endate1=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]} +$sixteen minutes" +"%Y-%m-%d %H:%M")

VAL3=$(date +%s -d"$endate1")
VAL4=$(date +%s -d"$friday123")

if [[ "$VAL3" > "$VAL4" ]]; then #19X
    hours_inbetween=`python3 ./busyday.py "$startdate1" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $ninteen - $hours_inbetween \))
    over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    python3 ./timer.py $over ${args[3]} "$currency1" "$startdate1" "$over"
    sleep 904
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') #How many lines exist in file.
    Sec=$(($filelength - 3))
    open1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick2.py $open1 $close1 $high1 $low1 $open $close $high $low $p
    sleep 1 
    curl -F "photo=@$p" -F "caption=$currency2" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
else
    left123=$(date -d "$(LC_TIME=C date -d "$startdate1")+$ninteen minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')   
    python3 ./timer.py $left123 ${args[3]} "$currency2" "$startdate1" "$left123"
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') #How many lines exist in file.
    Sec=$(($filelength - 3))
    open1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low1=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick2.py $open1 $close1 $high1 $low1 $open $close $high $low $p
    curl -F "photo=@$p" -F "caption=$currency2" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
    fi


startdate2=$(date -d "${args[1]}":"${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")
form2=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')
endate2=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]} +$sixteen minutes" +"%Y-%m-%d %H:%M")

VAL5=$(date +%s -d"$endate2")
VAL6=$(date +%s -d"$friday123")

if [[ "$VAL5" > "$VAL6" ]]; then #22X
    hours_inbetween=`python3 ./busyday.py "$startdate2" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form2`
    val=$(expr \( $twentiethree - $hours_inbetween \))
    overated=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    python3 ./timer.py $overated ${args[3]} "$currency3" "$startdate2" "$overated" 
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') 
    Two=$(($filelength - 3))
    Three=$(($filelength - 6))
    open=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick3.py $open3 $close3 $high3 $low3 $open2 $close2 $high2 $low2 $open $close $high $low $p
    curl -F "photo=@$p" -F "caption=$des3" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
else
    left12=$(date -d "$(LC_TIME=C date -d "$startdate1")+$twentiethree minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    python3 ./timer.py $left12 ${args[3]} "$des3" "$startdate2" "$left12"
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') 
    Two=$(($filelength - 3))
    Three=$(($filelength - 6))
    open=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$Sec') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low2=$(awk '{if(NR=='$Two') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    open3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low3=$(awk '{if(NR=='$Three') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick3.py $open3 $close3 $high3 $low3 $open2 $close2 $high2 $low2 $open $close $high $low $p
    curl -F "photo=@$p" -F "caption=$currency3" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
   fi
