#!/bin/bash

clear
if command -v pip >/dev/null 2>&1; then
    echo "PIP passed check"
    # i know some are not real, just to make sure lol
    sudo pip install discord==1.7.3
    sudo pip install discord.py==1.7.3
    sudo pip install asyncio
    sudo pip install datetime
    sudo pip install requests
    sudo pip install httpx
    sudo pip install pytube
    sudo pip install sys
    sudo pip install subprocess
    sudo pip install pytz
    echo "INSTALLATION COMPLETE!"
else
    echo "PIP did not pass check"
fi

