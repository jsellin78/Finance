#!/bin/bash

GROUP_ID=2012646742 #ChatID
BOT_TOKEN=5640166055:AAE4vMzP-lk2dh-fszrejyRFBhCCp1UCGXI #Token

# Send text message this way. For newline between messages add nl=$'\n'
# bash -c "/files/telegrambot.sh 'Hello $nl There!'"
# For Sending Photo instead of text add /sendPhoto instead of sendMessage in the curl request.

if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0` \"text message\""
  exit 0
fi

if [ -z "$1" ]
  then
    echo "Add message text as second arguments"
    exit 0
fi

if [ "$#" -ne 1 ]; then
    echo "You can pass only one argument. For string with spaces put it on quotes"
    exit 0
fi

curl -s --data "text=$1" --data "chat_id=$GROUP_ID" 'https://api.telegram.org/bot'$BOT_TOKEN'/sendMessage' > /dev/null