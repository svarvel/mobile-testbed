#!/data/data/com.termux/files/usr/bin/env bash
## NOTE: check if there is something to run 
## Author: Matteo Varvello (matteo.varvello@nokia.com)
## Date: 11/15/2021

# generate data to be POSTed to my server
generate_post_data(){
  cat <<EOF
    {
    "today":"${suffix}",
    "timestamp":"${current_time}",
    "uid":"${uid}",
    "uptime":"${uptime_info}",
    "debug":"${debug}",
    "msg":"${msg}"
    }
EOF
}

# check if user asked us to pause or not
user_file="/storage/emulated/0/Android/data/com.example.sensorexample/files/running.txt"
user_status="false"
if [ -f $user_file ]
then
	user_status=`sudo cat $user_file`
	if [ $user_status == "true" ]
	then
		echo "User pressed \"resume\""
		echo "false" > ".isDebug"
	else 
		echo "User pressed \"pause\""
		echo "true" > ".isDebug"
	fi
fi 

# check if debugging or production
if [ -f ".isDebug" ] 
then 
	debug=`cat .isDebug`
fi 

# inform server of reboot detected 
uptime_sec=`sudo cat /proc/uptime | awk '{print $1}' | cut -f 1 -d "."`
echo "Uptime: $uptime_sec sec"
if [ $uptime_sec -le 180 ] 
then
	suffix=`date +%d-%m-%Y`
	current_time=`date +%s`
	uid=`termux-telephony-deviceinfo | grep "device_id" | cut -f 2 -d ":" | sed s/"\""//g | sed s/","//g | sed 's/^ *//g'`
	uptime_info=`uptime`
	msg="reboot"
	echo "$(generate_post_data)"
	timeout 10 curl -s -H "Content-Type:application/json" -X POST -d "$(generate_post_data)" https://mobile.batterylab.dev:8082/status
fi 

# don't run if already running
ps aux | grep "state-update.sh" | grep "bash" > ".ps"
N=`cat ".ps" | wc -l`
if [ $N -eq 0 -a $debug == "false" ] 
then 
	echo "need to run"
	# inform server of restart needed
	suffix=`date +%d-%m-%Y`
	current_time=`date +%s`
	uid=`termux-telephony-deviceinfo | grep "device_id" | cut -f 2 -d ":" | sed s/"\""//g | sed s/","//g | sed 's/^ *//g'`
	uptime_info=`uptime`
	msg="script-restart"
	echo "$(generate_post_data)"
	timeout 10 curl -s -H "Content-Type:application/json" -X POST -d "$(generate_post_data)" https://mobile.batterylab.dev:8082/status

	# restart script 
	mkdir -p logs
	./state-update.sh > "logs/log-state-update-"`date +\%m-\%d-\%y_\%H:\%M`".txt" 2>&1 &
fi

# logging
echo `date +\%m-\%d-\%y_\%H:\%M` > ".last"
