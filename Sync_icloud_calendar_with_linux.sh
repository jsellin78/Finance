export APPLEID='' #appleid 
export APPLEPW='' #app password 


account_url=$(curl -s -X PROPFIND -u "$APPLEID:$APPLEPW" -H "Depth: 0" --data "<propfind xmlns='DAV:'><prop><current-user-principal/></prop></propfind>" https://caldav.icloud.com/ | grep -oP '(?<=<href xmlns="DAV:">/)\d+(?=/principal/)' | sed 's/^\s*//;s/\s*$//')


get_server_response=$(curl -s -X PROPFIND -u "$APPLEID:$APPLEPW" -H "Depth: 0"  --data "<propfind xmlns='DAV:' xmlns:cd='urn:ietf:params:xml:ns:caldav'><prop><cd:calendar-home-set/></prop></propfind>" https://caldav.icloud.com/$account_url/principal/)


server_url=$(echo "$get_server_response" | grep -oP '(?<=<href xmlns="DAV:">)https?://[^<]+(?=</href>)')


list_all_calenders=$(curl -s -X PROPFIND -u "$APPLEID:$APPLEPW" -H "Depth: 1"  --data "<propfind xmlns='DAV:'><prop><displayname/></prop></propfind>" $server_url | grep displayname)

info_about_each_calendar=$(curl -s -X PROPFIND -u "$APPLEID:$APPLEPW" -H "Depth: 1"  --data "<propfind xmlns='DAV:'><prop><displayname/></prop></propfind>" $server_url)

echo "account_url" $account_url 
echo "server_url: $server_url"
echo "list_all_calendars: $list_all_calenders"
echo "$info_about_each_calendar" | 
    grep -oP '(?<=<href>).+?(?=</href>)|(?<=<displayname>).+?(?=</displayname>)' | 
    awk 'NR%2{printf "%s ", $0; next;}1'


