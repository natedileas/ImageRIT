Requires:
software: numpy, cv2, python (obviously) 
hardare: a webcam that be acessed through opencv's VideoCapture Class (at position 0)

developed on windows, dell laptop, python 2.7, opencv 2

main.py is the main script (q to quit, s to save a screenshot, c to clear the list of transforms)
demo.avi is an example output video


To add a new function:
write a function that takes a frame and  returns it transformed
put this function in the 'transforms' folder
add lines to the __init__.py in that directory like this: 

from my_new_func import my_new_func
key2transforms.update({'k':my_new_func})

then when you run demo.py you'll be able to press the key and your function will be called