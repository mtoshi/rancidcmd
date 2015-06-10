#!/bin/sh

#
# rancid install
#

apt-get install -y rancid
cp -a utils/rancid/cloginrc ~/.cloginrc
chmod 700 ~/.cloginrc

#
# quagga install
#

apt-get install -y quagga=0.99.23-1

cp -a utils/quagga/*.conf /etc/quagga/
cp -a utils/quagga/daemons /etc/quagga/

service quagga restart
