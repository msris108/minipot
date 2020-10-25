Minipot Quickstart
==================
A simple honeypot to capture attacks such as netcat reverse shell attacks or reverse tcp shell attacks.
Minipot is written in python with no dependencies. Capable of simulating a simple shell and smart smart responses.

Installation
------------

    python -m pip install minipot

Install as Debian package:
--------------------------

Get the `.deb` from Github page, and run:

    sudo dpkg -i nanopot-1.0.0.0.deb

Config defaults to `/etc/var/minipot.ini`

Build Debian Pkg:
------------------
    dpkg-deb --build ./deb minipot-1.0.0.0.deb

install with

    sudo dpkg -i nanopot-1.0.0.0.deb

Running
-------

    python -m nanopot

Source Code
-----------

https://github.com/msris108/minipot

Documentation
-------------

https://minipot.rtfd.io