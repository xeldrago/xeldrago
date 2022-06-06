from PIL import Image 
b='pic path'
image_file = Image.open(b) # open colour image
image_file = image_file.convert('1') # convert image to black and white
image_file.save('B&W.jpg')