from PIL import Image 
b='10th.jpg'
image_file = Image.open(b) # open colour image
image_file = image_file.convert('2') # convert image to black and white
image_file.save('10th certificate B&W.jpg')