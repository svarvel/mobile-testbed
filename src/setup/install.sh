#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical

# stop sshd in case it was running
sv stop sshd 

apt-get -qy update
apt-get -qy -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" upgrade
apt-get -qy autoclean

# install and start ssh 
pkg install -y openssh cronie termux-services
sshd 
