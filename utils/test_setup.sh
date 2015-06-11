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

mkdir /etc/quagga
cp -a utils/quagga/*.conf /etc/quagga/
cp -a utils/quagga/daemons /etc/quagga/

apt-get install -y quagga
