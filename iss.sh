#!/bin/bash

dest="D:/M2CAD - source/iss/"
iss_list="D:/M2CAD - source/iss/iss_list.txt"

cnt=0

while IFS=',' read -r stan lnk stat
do
	if [ "$cnt" -eq 0 ]; then
		((cnt++))
		continue
	fi
	
	html=$(echo "$stan" | tr ':' '_')
	html+=".html"
	wget -O- --no-check-certificate "$lnk" > "$dest$html"

done < "$iss_list"

find "$dest" -name "*.html" -exec grep -A 7 ^.*TREN.* {} + | sed -e 's/<[^>]*>//g'
