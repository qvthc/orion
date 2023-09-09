#!/bin/bash

clear
if command -v pip >/dev/null 2>&1; then
    echo "PIP passed check"
    pip install discord
    pip install discord
    pip install json
    pip install asyncio
    pip install datetime
    pip install requests
    pip install httpx
    pip install pytube
    pip install sys
    pip install subprocess
    echo "INSTALLATION COMPLETE!"
else
    echo "PIP did not pass check"
fi
