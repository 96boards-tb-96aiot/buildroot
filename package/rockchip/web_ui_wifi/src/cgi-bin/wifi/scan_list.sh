#!/bin/sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin
wpa_cli -iwlan0 scan > /dev/null
wpa_cli -iwlan0  scan_result | awk '{print $5}' | sed '/^$/d' > /tmp/data_wifi_list
sed -i '1,2d' /tmp/data_wifi_list
echo ssid > /tmp/pub_name
data=`awk -vFS=, 'NR==FNR{split($0,a,FS);next}{split($0,b,FS);for(i in a){c[i]="\042"a[i]"\042:\042"b[i]"\042"};printf FNR==1?"[":",";$0="{"c[1]"}";printf $0}END{print "]"}' /tmp/pub_name /tmp/data_wifi_list`

echo $data > /tmp/wifi_list.txt
