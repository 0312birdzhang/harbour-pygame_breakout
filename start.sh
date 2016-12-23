#!/bin/sh
ps -ef|grep harbour-pygame_breakout|grep breakout.py|grep -v grep|awk '{print $2}'|xargs kill -9
cd /usr/share/harbour-pygame_breakout/py && python3 breakout.py