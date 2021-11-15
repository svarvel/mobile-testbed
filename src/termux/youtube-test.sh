#!/bin/bash
## NOTE: testing getting <<stats for nerds>> on youtube
## Author: Matteo Varvello (matteo.varvello@nokia.com)
## Date: 11/15/2021

# import utilities files needed
script_dir=`pwd`
adb_file=$script_dir"/adb-utils.sh"
source $adb_file
DURATION=30

# lower all the volumes
sudo media volume --show --stream 3 --set 0  # media volume
sudo media volume --show --stream 1 --set 0	 # ring volume
sudo media volume --show --stream 4 --set 0	 # alarm volume

# make sure screen is ON
turn_device_on

# launch YouTube 
am start -a android.intent.action.VIEW -d "https://www.youtube.com/watch?v=TSZxxqHoLzE"
sleep 1

# switch between portrait and landscape
# ?? 

# activate stats for nerds  
tap_screen 680 105 1 
tap_screen 370 1125 
exit -1 

# collect data 
t_s=`date +%s`
t_e=`date +%s`
let "t_p = t_s - t_e"
while [ $t_p -lt $DURATION ] 
do 
	# click to copy clipboard 
	tap_screen 592 216 1

	# dump clipboard 
	termux-clipboard-get
	t_e=`date +%s`
	let "t_p = t_s - t_e"
	sleep 1 
done

# stop playing 
sudo input keyevent KEYCODE_BACK
sleep 2 
tap_screen 670 1130 1 

# turn device off when done
turn_device_on
