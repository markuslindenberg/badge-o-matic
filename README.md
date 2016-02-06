# badge-o-matic self service badge printer

This repository contains the source code for the badge printer as used at [FFRL Routing Days](https://routingdays.ffrl.net/)

[Youtube video of printer in action](https://www.youtube.com/watch?v=dlJWirtAnGU&feature=youtu.be)

Main ingredients:

Hardware

* Brother QL-700 label printer (using QL-550 driver)
* BeagleBone Black

Software

* [Python 3](https://docs.python.org/3/library/)
* [Flask](http://flask.pocoo.org/)
* [Reportlab](http://www.reportlab.com/documentation/)

Dependencies: 

The badge printer was developed on a BeagleBone Black w/ Debian jessie.

* cups
* cups-bsd
* python3
* python3-flask
* python3-pil
* python3-reportlab

Some updated packages are needed from Debian unstable:

* printer-driver-ptouch (updated package w/ bugfixes)
* python3-pyroute2
* python3-reportlab
* python3-reportlab-accel

