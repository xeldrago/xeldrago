@echo off
:: Generate a random port between 1231 and 5698
set /a port=4588

:: Replace this with your actual Tailscale IP
set "TAILSCALE_IP=100.107.154.101"

echo Starting Python HTTP server on port %port%
echo Accessible via Tailscale at: http://%TAILSCALE_IP%:%port%
echo (Make sure your Tailscale IP is correct, and firewall allows incoming traffic)

:: Start server bound to all interfaces so it's reachable via Tailscale
start "XeldragoMusicServer" cmd /k python -m http.server %port% --bind 0.0.0.0

:: OPTIONAL: Open it in browser using your Tailscale IP
timeout /t 2 > nul
start http://100.107.154.101:%port%
