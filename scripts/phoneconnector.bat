ECHO OFF 
ECHO HELOW WORLD "biyuch"
adb kill-server
adb devices
adb tcpip 8080
adb connect 192.168.3.2
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.3.3
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.1.5
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.1.4
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.1.2
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.1.3
start /b E:\softwares\mobileconnector\scrcpy
adb connect 192.168.1.6
start /b E:\softwares\mobileconnector\scrcpy



