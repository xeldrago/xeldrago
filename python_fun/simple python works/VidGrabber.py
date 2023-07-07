import tkinter as tk
import requests
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tkinter.simpledialog import askstring

def download_video_with_requests():
    url = url_entry.get()
    filename = askstring("Save File", "Enter the file name:")
    if filename is None:
        return
    save_path = f'D:/Videos grabbed/{filename}.mp4'  # Replace with your desired save location
    
    try:
        # Use Selenium to retrieve the video source URL
        driver = webdriver.Chrome()  # Replace with the path to your Chrome WebDriver
        driver.get(url)
        driver.implicitly_wait(10)
        video_element = driver.find_element_by_tag_name('video')
        video_url = video_element.get_attribute('src')
        driver.quit()
        
        # Download the video using Requests
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        status_label.config(text='Video downloaded successfully.')
        
    except Exception as e:
        status_label.config(text='Error downloading video: ' + str(e))

def download_youtube_video_with_pytube():
    url = url_entry.get()
    filename = askstring("Save File", "Enter the file name:")
    if filename is None:
        return
    save_path = f'D:/Videos grabbed/{filename}.mp4'  # Replace with your desired save location
    
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(save_path)
        status_label.config(text='Video downloaded successfully.')
    except Exception as e:
        status_label.config(text='Error downloading video: ' + str(e))

# Create the main application window
window = tk.Tk()
window.title('Video Downloader')

# Create the URL input field and label
url_label = tk.Label(window, text='Enter video URL:')
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Create the download buttons
requests_button = tk.Button(window, text='Download with Requests (Selenium)', command=download_video_with_requests)
requests_button.pack()

pytube_button = tk.Button(window, text='Download from YouTube with Pytube', command=download_youtube_video_with_pytube)
pytube_button.pack()

# Create the status label
status_label = tk.Label(window, text='')
status_label.pack()

# Start the GUI event loop
window.mainloop()
