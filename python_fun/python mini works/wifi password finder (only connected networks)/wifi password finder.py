import os
net_id=input("type the network name connected to your device\n")
os.system(f"netsh wlan show profile {net_id} key=clear")
print("now from the output, look for key content, that is your lost or forgotten password")