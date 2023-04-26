#!/bin/bash
p="n43.png" #Image of Candlesticks
telegrambot="/root/newstart/telegrambot.sh"
sixteen="240"
ninteen="285"
twentiethree="330"
ted="19:00"
year=$(date +%Y)
month=$(date +%m)
#month=$(date -d "1 month ago" +'%m')
currency1="16x_15_minutes ${args[3]}"
currency2="19x_15_minutes ${args[3]}"
currency3="22x_4_minutes${args[3]}"
#pt="/root/tmp/${args[3]}155.txt"

# curl -F "photo=@$p" -F "caption=$des" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742'

# curl -F "photo=@$p" -F "caption=$desc1" 'https://api.telegram.org/bot$token/sendphoto?chat_id=$chatid'
args=("$@")


#hour      #minute                    #day  
startdate=$(date -d "${args[1]}":"${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M")

form=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]}" +"%Y-%m-%d %H:%M" | tr '-' ' ' | sed 's/.\{5\}$//')

endate=$(date -d "${args[1]}${args[2]} $year"-"$month"-"${args[0]} +$sixteen minutes" +"%Y-%m-%d %H:%M")

friday123=`python3 ./friday123.py $form` #prints the exact date of comming friday 

echo "friday is" $friday123
echo "form is" $form
VAL1=$(date +%s -d"$endate")
VAL2=$(date +%s -d"$friday123")

if [[ "$VAL1" > "$VAL2" ]]; then #
    echo "Pattern is greater than friday" #
    hours_inbetween=`python3 ./busyday.py "$startdate" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $sixteen - $hours_inbetween \))
    left_over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "final 16x pattern after weekend is" ${YELLOW}$left_over${YELLOW} $NOCOLOR
    #B=$(date -d "$(LC_TIME=C date -d "$left_over")+$val hour" +"%Y-%m-%d %H:%M") 
    echo "Pattern was created at"${NOCOLOR} ${YELLOW}$startdate${YELLOW} $NOCOLOR
    echo "Sunday is" $sunday
    echo "Friday is" $friday123 # "friday is " $friday
    echo "hours from startdate to friday close" $hours_inbetween
    echo $val "Missing hours from sunday to next week"  
    python3 ./timer.py $left_over ${args[3]} "$currency1" "$startdate" "$left_over"
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') #How many lines exist in file.
    open=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp${args[3]}155.txt" | jq '.Open' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    close=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Close' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    high=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.High' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    low=$(awk '{if(NR=='$filelength') print $0}' "/root/tmp/${args[3]}155.txt" | jq '.Low' | sed -e ':a;s/^.\{0,5\}$/&0/;ta')
    python3 ./candlestick1.py $open $close $high $low $p
    sleep 1  
    curl -F "photo=@$p" -F "caption=$currency1" 'https://api.telegram.org/bot6083852936:AAEOlpobL48v5aw0y11bqHVxsVdYOdvLhnw/sendphoto?chat_id=2012646742' > /dev/null
else
   echo "startdate" $startdate
   left=$(date -d "$(LC_TIME=C date -d "$startdate")+$sixteen minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ') #first pattern 16x  
   python3 ./timer.py $left ${args[3]} "$currency2" "$startdate" "$left"
   sleep 904 
   filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') #How many lines exist in file.
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
    echo "Pattern is greater than friday" #
    hours_inbetween=`python3 ./busyday.py "$startdate1" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form`
    val=$(expr \( $ninteen - $hours_inbetween \))
    over=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "final 19x pattern after weekend is" ${YELLOW}$over${YELLOW} $NOCOLOR
    echo "Pattern was created at"${NOCOLOR} ${YELLOW}$startdate1${YELLOW} $NOCOLOR
    echo "Sunday is" $sunday
    echo "Friday is" $friday123 # "friday is " $friday
    echo "hours from startdate to friday close" $hours_inbetween
    echo $val "Missing hours from sunday to next week"
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
    echo "startdate" $startdate
    left123=$(date -d "$(LC_TIME=C date -d "$startdate1")+$ninteen minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ') #first pattern 16x  
    echo "No weekend" $left123
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
    echo "Pattern is greater than friday" #
    hours_inbetween=`python3 ./busyday.py "$startdate2" "$friday123 $ted" | sed "s/\..*//"` 
    sunday=`python3 ./sunday.py $form2`
    val=$(expr \( $twentiethree - $hours_inbetween \))
    overated=$(date -d "$(LC_TIME=C date -d "$sunday")+$val minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "final 23x pattern after weekend is" ${YELLOW}$overated${YELLOW} $NOCOLOR
    echo "Pattern was created at"${NOCOLOR} ${YELLOW}$startdate1${YELLOW} $NOCOLOR
    echo "Sunday is" $sunday
    echo "Friday is" $friday123 # "friday is " $friday
    echo "hours from startdate to friday close" $hours_inbetween
    echo $val "Missing hours from sunday to next week"
    python3 ./timer.py $overated ${args[3]} "$currency3" "$startdate2" "$overated" 
    sleep 904 
    filelength=$(wc -l "/root/tmp/${args[3]}155.txt" | awk '{ print $1 }') #How many lines exist in file.
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
    echo "startdate" $startdate
    left12=$(date -d "$(LC_TIME=C date -d "$startdate1")+$twentiethree minutes" +"%Y-%m-%d %H:%M" | tr '-' ' ' | tr ':' ' ')  
    echo "No weekend" $left12
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
