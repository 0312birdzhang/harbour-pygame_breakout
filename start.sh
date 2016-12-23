#!/bin/sh
ps -ef|grep breakout.py|grep -v grep|awk '{print $2}'|xargs kill -9
cd /usr/share/harbour-pygame_breakout/py
sh -c "exec python3 breakout.py"
