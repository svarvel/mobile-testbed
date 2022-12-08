#!/data/data/com.termux/files/usr/bin/bash
## Date: 11/11/2021
## Author: Matteo Varvello (varvello@gmail.com)
## NOTE: script to run bunch of mtr tests (both ipv4 and ipv6)

# import common file
common_file=`pwd`"/common.sh"
if [ -f $common_file ]
then
	source $common_file
else
	echo "Common file $common_file is missing"
	exit -1
fi

# helper to run a test 
test(){
	prefix=$2
	myprint "Testing $prefix"
	#echo "==>    sudo mtr --no-dns --first-ttl 3 -r4wc $num $1     <=="
	timeout 60 sudo mtr --no-dns --first-ttl 3 -r4wc $num $1  >  $res_dir/$prefix-ipv4-$ts.txt 2>&1
	gzip $res_dir/$prefix-ipv4-$ts.txt
	if [ $use_v6 == "true" ]
	then
		ping6 -c 3 $1 > /dev/null 2>&1
		if [ $? -eq 0 ] 
		then 
			sudo mtr -r6wc $num $1   >  $res_dir/$prefix-ipv6-$ts.txt 2>&1
			gzip $res_dir/$prefix-ipv6-$ts.txt 
		fi 
	fi 
}

# input
if [ $# -eq 2 ]
then 
	suffix=$1
	ts=$2
else 
	suffix=`date +%d-%m-%Y`
	ts=`date +%s`
fi 

# folder organization
res_dir="mtrlogs/$suffix"
mkdir -p $res_dir
num=10
use_v6="false"

# logging
myprint "Starting MTR reporting. ResultsFolder: $res_dir"

# popular providers
myprint "Testing popular content providers: [google, facebook, amazon]"
test google.com google 
test facebook.com facebook
test amazon.com amazon

# popular DNS
myprint "Testing popular DNS: [google, cloudflare]"
sudo mtr --no-dns --first-ttl 3 -r4wc $num 8.8.8.8 >  $res_dir/google-dns-ipv4-$ts.txt 2>&1
gzip $res_dir/google-dns-ipv4-$ts.txt
sudo mtr --no-dns --first-ttl 3 -r4wc $num 1.1.1.1 >  $res_dir/cloudflare-dns-ipv4-$ts.txt 2>&1
gzip $res_dir/cloudflare-dns-ipv4-$ts.txt 
if [ $use_v6 == "true" ]
then 
	sudo mtr -r6wc $num 2001:4860:4860::8888 >  $res_dir/google-dns-ipv6-$ts.txt 2>&1
	gzip $res_dir/google-dns-ipv6-$ts.txt 
	sudo mtr -r6wc $num 2606:4700:4700::1111 >  $res_dir/cloudflare-dns-ipv6-$ts.txt 2>&1
	gzip $res_dir/cloudflare-dns-ipv6-$ts.txt 

fi 

# test youtube right before youtube test (to better correlated)
test youtube.com youtube

# logging 
t_e=`date +%s`
let "t_p = t_e - t_s"
myprint "Done MTR reporting. Duration: $t_p. ResFolder: $res_dir"
