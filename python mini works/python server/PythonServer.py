import os
import socket
import webbrowser


# getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
#getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
#printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")
q=input("tell me a port number that you want your site deployed at\n") #getting port number from user
p=print("take a note of your ipv4 for filling it in the URL")


print("your website or folders will be served now")





chrome_path = 'C:\"Program Files"\Google\Chrome\Application\chrome.exe %s'


url=f"http://{ip_address}:{q}/"
webbrowser.get(chrome_path).open(url)

os.system(f"python -m http.server {q}")

print("reload browser if you see it not loading properly")
