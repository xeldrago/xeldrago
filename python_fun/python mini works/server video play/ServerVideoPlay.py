import ffmpeg
import os

os.system("pythonserver")

#stream from server

video_format = "flv"
server_url = "http://192.168.1.10:7878/"

process = (ffmpeg.input("vadachennaiCut2.mp4").output(server_url, codec = "copy",videolisten=1,f=video_format).global_args("-re").run())


