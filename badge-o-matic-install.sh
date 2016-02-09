#!/bin/bash

#================================================================
#
#    This installs badge-o-matic with its dependencies
#    on debian jessie
#
#================================================================


# add unstable repository
cat <<EOT > /etc/apt/sources.list.d/sid.list
deb http://ftp.de.debian.org/debian/ sid main non-free contrib
deb-src http://ftp.de.debian.org/debian/ sid main non-free contrib
EOT

# apt pinning for unstable packages
cat <<EOT > /etc/apt/preferences.d/sid
Package: *
Pin: release a=unstable
Pin-Priority: 20

Package: printer-driver-ptouch
Pin: release a=unstable
Pin-Priority: 600

Package: python3-pyroute2
Pin: release a=unstable
Pin-Priority: 600

Package: python3-reportlab
Pin: release a=unstable
Pin-Priority: 600

Package: python3-reportlab-accel
Pin: release a=unstable
Pin-Priority: 600
EOT

apt-get update

# install packets from stable
apt-get install git cups cups-bsd python3 python3-flask python3-pil

# install packets from unstable
apt-get install printer-driver-ptouch python3-pyroute2 python3-reportlab python3-reportlab-accel

# get badge-o-matic from github
git clone --depth 1 git@github.com:markuslindenberg/badge-o-matic.git

