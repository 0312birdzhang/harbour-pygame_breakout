#!/bin/sh
ps -ef|grep harbour-pygame_breakout|grep breakout.py|grep -v grep|awk '{print $2}'|xargs kill -9