#!/bin/bash
## Author: Matteo Varvello 
## Date:   11/10/2021


# import utilities files needed
script_dir=`pwd`
adb_file=$script_dir"/adb-utils.sh"
source $adb_file
toggle_wifi "off"
timeout 5 /usr/bin/ifconfig wlan0 > wlan-info 2>&1
echo $?
sleep 5 
toggle_wifi "on"
exit -1 
sudo input keyevent KEYCODE_HOME
echo "[toggle_wifi] swipe down"
sudo input swipe 370 0 370 500
sleep 5
echo "[toggle_wifi] press"
sudo input tap 300 100
sleep 2 
echo "[toggle_wifi] swipe up"
sudo input swipe 370 500 370 0

echo "[toggle_wifi] swipe down"
sudo input swipe 370 0 370 500
sleep 5
echo "[toggle_wifi] press"
sudo input tap 300 100
sleep 2 
echo "[toggle_wifi] swipe up"
sudo input swipe 370 500 370 0


