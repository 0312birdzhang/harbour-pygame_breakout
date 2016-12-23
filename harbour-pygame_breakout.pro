# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = harbour-pygame_breakout



sh.path = /usr/share/$$TARGET
sh.files += start.sh \
            stop.sh
INSTALLS += sh

py.path = /usr/share/$$TARGET/py
py.files += py/breakout.py

INSTALLS += py

CONFIG += sailfishapp

SOURCES += src/harbour-pygame_breakout.cpp

OTHER_FILES += rpm/harbour-pygame_breakout.changes \
    rpm/harbour-pygame_breakout.spec \
    rpm/harbour-pygame_breakout.yaml \
    harbour-pygame_breakout.desktop

SAILFISHAPP_ICONS = 86x86 108x108 128x128 256x256




