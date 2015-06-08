#!/bin/sh

#
# rancid install
#

apt-get install -y rancid
cp -a utils/rancid/cloginrc ~/.cloginrc

#
# quagga install
#

apt-get install -y quagga

cp -a utils/quagga/*.conf /etc/quagga/
cp -a utils/quagga/daemons /etc/quagga/

service quagga restart
