#!/data/data/com.termux/files/usr/bin/env bash
## Note:   Script to automate videoconferencing clients
## Author: Matteo Varvello
## Date:   11/29/2021


# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
function ctrl_c() {
	safe_stop
	exit -1 
}

safe_stop(){
	sudo pm clear $package
	echo "done" > ".videoconfstatus"
	echo "false" > ".to_monitor"
	sudo killall tcpdump
}

# generate data to be POSTed to my server
generate_post_data(){
  cat <<EOF
    {
    "today":"${suffix}",
    "timestamp":"${current_time}",
    "uid":"${uid}",
    "cpu_util_midload_perc":"${cpu_usage_middle}",
    "bdw_used_MB":"${traffic}",
    "tshark_traffic_MB":"${tshark_size}", 
    "msg":"${msg}"
    }
EOF
}

# send report to our server 
send_report(){
	current_time=`date +%s`
	msg="ALL-GOOD"
	myprint "Sending report to the server: "
	echo "$(generate_post_data)" 
	timeout 15 curl -s -H "Content-Type:application/json" -X POST -d "$(generate_post_data)"  https://mobile.batterylab.dev:8082/videoconftest
}

# import utilities files needed
DEBUG=1
adb_file=`pwd`"/adb-utils.sh"
source $adb_file

# sync barrier between devices 
sync_barrier(){
    myprint "Time for sync barrier..."
	echo "ready" > ".localsync" 
	isSync=0
	while [ $use_sync == "true" -a $isSync -eq 0 ] 
	do 
		if [ -f ".globalsync" ] 
		then
			isSync=1
		fi 
		sleep 0.5
	done
    myprint "We are sync!" 
}

# make sure a device is unlocked 
unlock_device(){
	# check if device is locked or not
	foreground=`sudo dumpsys window windows | grep -E 'mCurrentFocus' | cut -d '/' -f1 | sed 's/.* //g'`
	if [[ "$foreground" == *"StatusBar"* ]]
	then
		myprint "Device is locked. Exiting!"
		exit -1 
	fi
}


# find package and verify videconferencing app is installed 
find_package(){
    if [ $app == "zoom" ]
    then 
        package="us.zoom.videomeetings"
    elif [ $app == "webex" ]
    then 
        package="com.cisco.webex.meetings"        
    elif [ $app == "meet" ]
    then 
        package="com.google.android.apps.meetings"        
    else 
        myprint "$app is currently not supported"
        exit -1
    fi 

    # make sure app is installed? 
    pm list packages -f | grep $package > /dev/null 
    if [ $? -ne 0 ] 
    then 
        myprint "Something is wrong. Package $package was not found. Please install it" 
        exit -1
    else 
		myprint "Package $package correctly found!"
	fi 
}

# grant permission required by each app
## adb shell dumpsys package com.cisco.webex.meetings | grep permission
grant_permission(){
    if [ $app == "zoom" ]
    then 
        sudo pm grant $package android.permission.RECORD_AUDIO
        sudo pm grant $package android.permission.WRITE_EXTERNAL_STORAGE
        sudo pm grant $package android.permission.CAMERA
    elif [ $app == "webex" ]
    then 
        sudo pm grant $package android.permission.RECORD_AUDIO
        sudo pm grant $package android.permission.WRITE_EXTERNAL_STORAGE
        sudo pm grant $package android.permission.CAMERA
        sudo pm grant $package android.permission.READ_CONTACTS
        sudo pm grant $package android.permission.CALL_PHONE
        sudo pm grant $package android.permission.ACCESS_FINE_LOCATION
    elif [ $app == "meet" ]
    then 
        sudo pm grant $package android.permission.RECORD_AUDIO
        sudo pm grant $package android.permission.CAMERA        
        sudo pm grant $package android.permission.CALL_PHONE
    fi 
}

# wait for a specific screen id (only zoom for now)  
wait_for_screen(){
	status="failed"
	screen_name=$1
	MAX_ATTEMPTS=10
	foreground=`sudo dumpsys window windows | grep -E 'mCurrentFocus' | cut -d '/' -f2 | awk -F "." '{print $NF}' | sed 's/}//g'`
	while [ $foreground != $screen_name ]
	do 
		let "c++"
		sleep 2 
		foreground=`sudo dumpsys window windows | grep -E 'mCurrentFocus' | cut -d '/' -f2 | awk -F "." '{print $NF}' | sed 's/}//g'`
		if [ $c -eq $MAX_ATTEMPTS ]
		then
			break
		fi 
	done
	status="success" #FIXME -- manage unsuccess 
	sleep 2 	
}


# helper function to join a zoom meeting
run_zoom(){
	# click on "join a meeting"
	wait_for_screen "WelcomeActivity"
	tap_screen $x_center 1020 5
	 
	# enter meeting ID
	wait_for_screen "JoinConfActivity"
	sudo input text "$meeting_id" 
	tap_screen $x_center 655 5
	
	# enter password if needed
	wait_for_screen "ConfActivityNormal"
	sleep 5 
	if [ -z $password ]
	then 
		myprint "Password not provided. Verify on screen if needed or not" 
	else 
		myprint "Entering Password: $password" 
		sudo input text "$password" 
		sleep 1
		tap_screen 530 535 5
	fi 

	# sync barrier (testing )
	if [ $sync_time != 0 ]
	then 
		t_now=`date +%s`
		let "t_sleep = sync_time - t_now"
		if [ $t_sleep -gt 0 ]
		then
			myprint "Sleeping $t_sleep to sync up!"
			sleep $t_sleep
		fi 
	fi 
	
	# click join with video or not
	if [ $use_video == "true" ] 
	then 
		y_coord="1040"   
	else 
		y_coord="1180"     
	fi 
	tap_screen $x_center $y_coord 5
	
	# click to join audio
	myprintn "click to join audio"
	tap_screen 200 1110 3
	tap_screen 178 1110
	
	# # MUTE! -- FIXME 
	# use_mute="true"	
	# if [ $use_mute == "true" ] 
	# then 
	# 	sudo input tap 75 1225 && sleep 0.2 && sudo input tap 75 1225
	# fi 
}

# helper function to join a webex meeting
run_webex(){
	if [ $clear_state == "true" ] 
	then 
		tap_screen 560 785 2 
		tap_screen 594 922 2
	fi 

	# enter meeting ID
	tap_screen $x_center 935 3
	sudo input text "$meeting_id"
	 
	# add user and password on first run
	if [ $clear_state == "true" ] 
	then 
		tap_screen $x_center 500 2
		sudo input text "Bravello"
		tap_screen $x_center 620 2
		sudo input text "bravello@gmail.com"
		sleep 2 
	fi 

	# click "JOIN"
	tap_screen 645 105 5

	# accept what needed
	if [ $clear_state == "true" ] 
	then 
		myprint "Accept what needed..."
		tap_screen 515 1055 2
		tap_screen 405 1055 2
	fi 
	
	# join with video/audio or not
	y_coord=1180
	if [ $use_video == "true" ] 
	then 
		myprint "Turning on video..."
		tap_screen 280 $y_coord 2
	fi  
	if [ $use_mute == "true" ] 
	then 
		tap_screen 160 $y_coord 2
	fi 
	
	# allow extra time when master script is not blocking
	if [ $video_recording == "true" ]
	then 
	  myprint "Give extra 5 seconds to host to setup meeting (since video recording is not blocking)"
	  sleep 5 
	fi 

	# sync barrier 
	myprint "Skipping sinc barrier"
	#sync_barrier
	sleep 5 	

	# press join
	tap_screen 485 $y_coord 8
	
	# accept warning -- unused? 
	#tap_screen 375 1075 3

	# go full screen (which is comparable with zoom default)
	if [ $change_view == "false" ]
	then 
		sudo input tap 200 400 & sleep 0.1; sudo input tap 200 400
	fi 
}

# helper function to join a google meet meeting
run_meet(){
	if [ $clear_state == "true" ] 
	then 
		tap_screen $x_center 1090 5 # FIXME: maybe even more? 
	fi 

	# click on "join a meeting" 
	tap_screen 515 230 3
	 
	# enter meeting ID
	sudo input text "$meeting_id" #FIXME - check DVPN code (verify spaces) 
	tap_screen 640 105 3
	 
	# enter password if needed
	if [ -z $password ]
	then 
		myprint "Password not provided. Verify on screen if needed or not" 
	else 
		sudo input text "$password"
		tap_screen 530 780 1
	fi 

	# sync barrier 
	myprint "Skipping sync barrier"
	#sync_barrier
	sleep 5 
	
	# join with video or not
	if [ $use_video == "false" ] 
	then 
		tap_screen 175 855 1 
	fi 
	if [ $use_mute == "true" ] 
	then 
		tap_screen 295 855 1
	fi 

	# press join
	tap_screen 485 855 5

	# get full screen (comparable with zoom)
	tap_screen $x_center $y_center
}

# leave zoom call
leave_zoom(){
	tap_screen $x_center $y_center 1
	tap_screen 630 122 3
	tap_screen $x_center 280
}

# leave webex call
leave_webex(){
    if [ $change_view != "true" ]
    then
        tap_screen $x_center $y_center
    fi
	tap_screen 534 1200 2
	tap_screen 400 1056
}

# leave meet call
leave_meet(){
    if [ $change_view != "true" ]
    then
        tap_screen $x_center $y_center
    fi 
	tap_screen 130 1180
}

# script usage
usage(){
    echo "====================================================================================================================================================================="
    echo "USAGE: $0 -a/--app, -p/--pass, -m/--meet, -v/--video, -D/--dur, -c/--clear, -i/--id, --pcap, --iface, --remote, --vpn, --view,  --uid, --sync"
    echo "====================================================================================================================================================================="
    echo "-a/--app        videoconf app to use: zoom, meet, webex" 
    echo "-p/--pass       zoom meeting password" 
    echo "-m/--meet       zoom meeting identifier" 
    echo "-v/--video      turn camera on (enable flag, default=false)" 
    echo "-D/--dur        call duration" 
    echo "-c/--clear      clear zoom state (enable flag, default=false)" 
    echo "-i/--id         test identifier to be used" 
    echo "--suffix        folder identifier for results" 
    echo "--pcap          request pcap collection"
	echo "--iface         current interface in use"  
    echo "--remote        start a remote client in Azure"
    echo "--rec           record video of the screen"
    echo "--view          change from default view"
    echo "--uid           IMEI of the device"
    echo "--sync          future time to sync"
    echo "====================================================================================================================================================================="
    exit -1
}

# general parameters
clear_state="true"                       # clear zoom state before the run 
use_video="false" 	                     # flag to control video usage or not 
package=""                               # package of videoconferencing app to be tested
duration=10                              # default test duration before leaving the call
phone_info=$base_dir"/phones-info.json"  # json file containing device information 
suffix=`date +%d-%m-%Y`                  # folder id (one folder per day)
test_id=`date +%s`                       # unique test identifier 
pcap_collect="false"                     # flag to control pcap collection ar router
iface="wlan0"                            # current default interface where to collect data
use_monsoon="false"                      # flag to control monsoon usage or not (battery measurements)
remote="false"                           # start a remote client in Azure 
use_vpn="false"                          # flag to control if to use a VPN or not
video_recording="false"                  # record screen or not 
change_view="false"                      # change from default view 
turn_off="false"                         # turn off the screen 
big_packet="false"                       # keep track if big packet size was passed 
use_mute="false"                         # FIXME 
uid="none"                               # user ID
sync_time=0                              # future sync time 

# read input parameters
while [ "$#" -gt 0 ]
do
    case "$1" in
        -a | --app)
            shift; app="$1"; shift;
            ;;
        -p | --pass)
            shift; password="$1"; shift;
            ;;
        -m | --meet)
            shift; meeting_id="$1"; shift;
            ;;
        -v | --video)
            shift; use_video="true";
            ;;
        -h | --help)
            usage
            ;;
		-D | --dur)
			shift; duration="$1"; shift;
			;;
		--iface)
			shift; iface="$1"; shift;
			;;
        --suffix)
            shift; suffix="$1"; shift;
            ;;
        --big)
            shift; big_packet_size="$1"; big_packet="true"; shift;
            ;;
        -c | --clear)
            shift; clear_state="true";
            ;;
        -i | --id)
            shift; test_id="$1"; shift;
            ;;
        --pcap)
            shift; pcap_collect="true";
            ;;
        --remote)
            shift; remote="true";
            ;;
        --rec)
            shift; video_recording="true";
            ;;
        --view)
            shift; change_view="true";
            ;;
        --off)
            shift; turn_off="true"; 
            ;;      
        --uid)
        	shift; uid="$1"; shift;
            ;;
        --sync)
        	shift; sync_time="$1"; shift;
            ;;
        -*)
            echo "ERROR: Unknown option $1"
            usage
            ;;
    esac
done

# make sure only this instance of this script is running
my_pid=$$
myprint "My PID: $my_pid"
ps aux | grep "$0" | grep "bash" > ".ps-videoconf"
N=`cat ".ps-videoconf" | wc -l`
if [ $N -gt 1 ]
then
    while read line
    do
        pid=`echo "$line" | awk '{print $2}'`
        if [ $pid -ne $my_pid ]
        then
            myprint "WARNING. Found a pending process for $0. Killing it: $pid"
            kill -9 $pid
        fi
    done < ".ps-videoconf"
fi

# update UID if needed 
if [ $uid == "none" ]
then 
	uid=`termux-telephony-deviceinfo | grep device_id | cut -f 2 -d ":" | sed s/"\""//g | sed s/","//g | sed 's/^ *//g'`
fi 
myprint "UID: $uid"

# clean sync files 
use_sync="true"
clean_file ".videoconfstatus"
clean_file ".localsync" 
clean_file ".globalsync" 

# lock this device 
touch ".locked"

# check meeting id was correctly passed
if [ -z "$meeting_id" -a $remote == "false" ]
then 
    myprint "ERROR. Missing meeting identifier (-m/--meet)"
	exit -1
fi 

# get big packet size if it was not passed 
if [ $big_packet == "false" ] 
then 
	big_packet_size=400
	if [ $app == "meet" ] 
	then 
		big_packet_size=500
	fi 
fi 

# get private  IP in use 
my_ip=`ifconfig $iface | grep "\." | grep -v packets | awk '{print $2}'`

# screen info
width="720"
height="1280"
let "x_center = width/2"
let "y_center = height/2"

# check that app is supported and find its package 
find_package

# folder organization
res_folder="./videoconferencing/${suffix}"
mkdir -p $res_folder 

# # ntp update  # currently not supported on termux
# use_ntp="false"
# if [ $use_ntp == "tru" ] 
# then 
# 	sudo ntpdate 0.us.pool.ntp.org
# fi 

# make sure screen is on
turn_device_on

# make sure device is on and unlocked # no need
unlock_device

# clear app states and  re-grant permissions
if [ $clear_state == "true" ] 
then 
	sudo pm clear $package
fi 

# allow permission
grant_permission

# close all pending apps
close_all

# start pcap collection if needed
if [ $pcap_collect == "true" ] 
then 
    pcap_file="${res_folder}/${test_id}.pcap"
    tshark_file="${res_folder}/${test_id}.tshark"
    if [ $app == "zoom" ] 
	then 
		port_num=8801
	elif [ $app == "meet" ] 
	then 
		port_num=19305
	elif [ $app == "webex" ] 
	then 
		port_num=9000
	fi 
	sudo tcpdump -i $iface port $port_num -w $pcap_file > /dev/null 2>&1 & 
	disown -h %1 # what is this doing?
	myprint "Started tcpdump: $pcap_file Interface: $iface Port: $port_num BigPacketSize: $big_packet_size"
fi 

# start background procees to monitor CPU on the device
log_cpu=$res_folder"/"$test_id".cpu"
log_cpu_top=$res_folder"/"$test_id".cpu_top"
clean_file $log_cpu
clean_file $log_cpu_top
low_cpu="false"
myprint "Starting cpu monitor. Log: $log_cpu LowCpu: $low_cpu"
echo "true" > ".to_monitor"
clean_file ".ready_to_start"
cpu_monitor $log_cpu &
cpu_monitor_top $log_cpu_top &

# get initial network data information
interface=$iface
compute_bandwidth
traffic_rx=$curr_traffic
traffic_rx_last=$traffic_rx

# cleanup logcat
sudo logcat -c 

# start app 
t_launch=`date +%s` #NOTE: use posterior time in case u want to filter launching and joining a conference
myprint "Launching $app..."
sudo monkey -p $package 1 > /dev/null 2>&1

# allow time for app to launch # FIXME 
sleep 5 

# needed to handle warning of zoom on rooted device 
if [ $clear_state == "true" -a $app == "zoom" ] 
then
	wait_for_screen "LauncherActivity"	
	sudo input tap 435 832
fi 

# join a meeting in the app to be tested
user="azureuser"
server="168.61.166.242"
key="$HOME/.ssh/id_rsa_azure"
if [ $app == "zoom" ]
then 
	if [ $remote == "true" ] 
	then
		#meeting_id="259\ 888\ 3628"
		meeting_id="689\ 356\ 0343"
		password="abc"
		myprint "Starting $app remote client..."
		ssh -o StrictHostKeyChecking=no  -i $key -f $user@$server "./zoom.sh start $test_id"
		remote_exec="./zoom.sh"
		sleep 5
	fi 
	run_zoom 
elif [ $app == "webex" ]
then 
	if [ $remote == "true" ] 
	then
		meeting_id="1325147081"
		myprint "Starting $app remote client..."
		ssh -o StrictHostKeyChecking=no -i $key -f $user@$server "./webex.sh start $test_id"
		remote_exec="./webex.sh"
		sleep 15
	fi
    run_webex
elif [ $app == "meet" ]
then 
	if [ $remote == "true" ] 
	then
		meeting_id="fnu-xvxb-fdj"
		myprint "Starting $app remote client..."
		ssh -o StrictHostKeyChecking=no -i $key -f $user@$server "./googlemeet.sh start $test_id"
		remote_exec="./googlemeet.sh"
		sleep 10
	fi 
    run_meet
fi 
t_actual_launch=`date +%s`

# change the view to multi windows 
if [ $change_view == "true" ]
then 
    myprint "A view change was requested!"
    if [ $app == "zoom" ] 
    then 
        sudo input swipe 700 800 300 800
    elif [ $app == "meet" ] # -o $app == "webex" ] #CHECK: webex is naturally multi-view
    then 
        tap_screen $x_center $y_center
    fi
fi 

# turn off the screen 
if [ $turn_off == "true" ] 
then 
    turn_device_off
fi 

# manage screen recording
if [ $video_recording == "true" ]
then
    # rotate screen 
	if [ $app != "zoom" ] # cause zoom ignores this
	then 
		myprint "Rotating screen in landscape mode..."
		sudo content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1
		sleep 5
	fi 

    # make sure video is full screen 
	if [ $app == "webex" ] 
	then 
		sudo input tap 730 250 & sleep 0.1; sudo input tap 730 250
	elif [ $app == "meet" ]
	then 
    	tap_screen 1200 430 
	fi 
	
    # skip first 60 seconds when screen is black anyway 
    myprint "Skip first 60 seconds since screen is black anyway"
    sleep 60
    
	# start recording the video 
    screen_video="${res_folder}/video-rec-${test_id}"
    myprint "Start video recording: $screen_video"
    (sudo screenrecord $screen_video".mp4" --time-limit $duration &)
fi

# wait for test to end 
myprint "Waiting $duration for experiment to end..."
sleep 5 

# REDO go full screen (which is comparable with zoom default) -- sometimes fails...
if [ $change_view == "false" -a $app == "webex" ]
then 
    myprint "Redoing tap for full screen, just in case. Verify no issue added" 
    sudo input tap 200 400 & sleep 0.1; sudo input tap 200 400
fi

# sleep up to mid experiment then take a screenshot 
let "half_duration = duration/2 - 5"
sleep $half_duration 
sudo screencap -p $res_folder"/"$test_id".png" 
sudo chown $USER:$USER $res_folder"/"$test_id".png"

# sleep rest of the experiment
sleep $half_duration 
sudo chown $USER:$USER $res_folder"/"$test_id".png"

# close remote client if needed
if [ $remote == "true" ] 
then
	myprint "Stopping $app remote client..."
	echo "ssh -o StrictHostKeyChecking=no -i $key -f $user@$server \"$remote_exec stop\""
	ssh -o StrictHostKeyChecking=no -i $key -f $user@$server "$remote_exec stop"
fi 

# stop tcpdump 
if [ $pcap_collect == "true" ] 
then 
	sudo killall tcpdump 
	myprint "Stopped tcpdump. Starting background analysis: $pcap_file"
	#echo "=> tcpdump -r $pcap_file -ttnn | python measure.py $res_folder $test_id $my_ip $big_packet_size" 
	tcpdump -r $pcap_file -ttnn | python measure.py $res_folder $test_id $my_ip $big_packet_size & 
fi 

# leave the meeting 
myprint "Close $app..."
if [ $app == "zoom" ]
then 
   leave_zoom
elif [ $app == "webex" ]
then 
	leave_webex
elif [ $app == "meet" ]
then 
	leave_meet
fi 
if [ $clear_state == "true" ] 
then 
	sudo pm clear $package
fi 
echo "done" > ".videoconfstatus"
t_now=`date +%s`

# stop CPU
myprint "Done monitoring CPU"
echo "false" > ".to_monitor"

# collect logcat #FIXME (add analysis for meet I believe?)
log_cat="${res_folder}/${test_id}.logcat"
sudo logcat -d > $log_cat
# if 'IMC' in line and 'Statistics' in line and 'Encoded' not in line:

# tshark analysis 
if [ $pcap_collect == "true" ] 
then 
	myprint "Starting tshark analysis: $tshark_file"
	tshark -nr $pcap_file -T fields -E separator=',' -e frame.number -e frame.time_epoch -e frame.len -e ip.src -e ip.dst -e ipv6.dst -e ipv6.src -e _ws.col.Protocol -e tcp.srcport -e tcp.dstport -e tcp.len -e tcp.window_size -e tcp.analysis.bytes_in_flight  -e tcp.analysis.ack_rtt -e tcp.analysis.retransmission  -e udp.srcport -e udp.dstport -e udp.length > $tshark_file 
	tshark_size=`cat $tshark_file | awk -F "," -v my_ip=$my_ip '{if($4!=my_ip){if($8=="UDP"){tot_udp += ($NF-8);} if($8=="TCP"){tot_tcp += ($11);}}}END{tot=(tot_tcp+tot_udp)/1000000; print "TOT:" tot " TOT-TCP:" tot_tcp/1000000 " TOT-UDP:" tot_udp/1000000}'`
	# clean pcap when done
	ps aux | grep measure.py | grep -v "grep" > /dev/null
	ans=$?
	c=0
	while [ $ans -eq 0 -a $c -lt 30 ] 
	do 
		ps aux | grep measure.py | grep -v "grep" > /dev/null
		ans=$?
		sleep 2
		let "c++"
	done
	myprint "Cleaning PCAP file"
	sudo rm $pcap_file
fi 

# update traffic rx (for this URL)
compute_bandwidth $traffic_rx_last
traffic_rx_last=$curr_traffic

# log results
median_cpu="N/A"
let "call_duration = t_now - t_actual_launch"
log_traffic=$res_folder"/"$test_id".traffic"
echo -e "$app_traffic\t$pi_traffic" > $log_traffic

# send report to the server
send_report

# return HOME and turn off screen 
sudo input keyevent HOME
turn_device_off
clean_file ".locked"