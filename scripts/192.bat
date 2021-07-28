ECHO OFF 
ECHO HELOW WORLD "biyuch"
adb kill-server
adb devices
adb tcpip 5555
adb connect 192.168.3.4
start /b E:\softwares\mobileconnector\scrcpy
