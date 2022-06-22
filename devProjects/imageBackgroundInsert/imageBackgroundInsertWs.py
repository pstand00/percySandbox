# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:09:59 2022

@author: Pete
"""

# test to take an image and post it on a x by y 
from PIL import Image, ImageDraw

# dimensions allowed by instagram 
# width 
# height 

# landscape: 1080 X 608 (1.91:1 ratio)
# portrate: 1080 x 1350 (4:5 ratio)

# define which is higher 
# then define as variable: landscape or portrait

# first test [create a square]
w, h = 1000, 1000
shape = [(0, 0), (w, h)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
  
# creating new Image object
img = Image.new("RGB", (w, h))
  
# create rectangle image
img1 = ImageDraw.Draw(img)  
img1.rectangle(shape, fill ="white")
img.show()


# second test [create a square & overlay an image]
# ===========================================================================
# append an image to that square 
topImage = Image.open("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final3.png")
widthTop, heightTop = topImage.size 
# create white square
widthRect, heightRect = heightTop, heightTop
shape = [(0, 0), (widthRect, heightRect)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
# creating new Image object
rectImage = Image.new("RGB", (widthRect, heightRect))
  
# create rectangle image
rectImageDraw = ImageDraw.Draw(rectImage)  
rectImageDraw.rectangle(shape, fill ="white")
rectImage.show()

# merge the images 
rectImageMerge = rectImage
# will need to use the following equation for landscape mode .... int((widthRect - widthTop) / 2)
rectImageMerge.paste(topImage, (int((widthRect - widthTop) / 2), 0), topImage)
rectImageMerge.show()

# third test [make the sizing dynamic]
# ===========================================================================
# define how extreme we can get with the width or height of our picture
# using this as my source, but need to stay current:
# https://colorlib.com/wp/size-of-the-instagram-picture/
# Instagram Landscape (horizontal) Photo	1080 X 608 (1.91:1 ratio)
# Instagram Portrait	1080 x 1350 (4:5 ratio)
landscapeRatio = (1 / 1.91)
portraitRatio = (4 / 5)

# actually load the images 
# topImage = Image.open("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final3.png")
# square version 
topImage = Image.open("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final2.png")
# landscape version
topImage = Image.open("C:\\Users\\Pete\\Documents\\Projects\\Dynamic Cropping Test\\final1.png")

widthTop, heightTop = topImage.size 
if widthTop > heightTop:
    orientation = 'Landscape'
    # check if the current dimensions meet the min 
    if heightTop < landscapeRatio * widthTop:
        print('image isnt square enough ')
        # create background shape (white color)
        widthRect, heightRect = widthTop, (landscapeRatio * widthTop)
        shape = [(0, 0), (widthRect, heightRect)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
        rectImage = Image.new("RGB", (widthRect, int(heightRect)))
        # create rectangle image
        rectImageDraw = ImageDraw.Draw(rectImage)  
        rectImageDraw.rectangle(shape, fill ="white")
        # rectImage.show()
        # place the top image 
        rectImageMerge = rectImage
        # will need to use the following equation for landscape mode .... int((widthRect - widthTop) / 2)
        rectImageMerge.paste(topImage, (0, int((heightRect - heightTop) / 2)), topImage)
        rectImageMerge.show()
        # save the image as "screenshot_padding.png"
    else: 
        print('image is square enough')
        # save the image as "screenshot_padding.png"
else:
    orientation = 'Portrait'
    if widthTop < portraitRatio * heightTop:
        print('image isnt square enough ')
        # create background shape (white color)
        widthRect, heightRect = (portraitRatio * heightTop), heightTop
        shape = [(0, 0), (widthRect, heightRect)] # where 0, 0 is the starting point and # w, h is the size of the rectangle 
        rectImage = Image.new("RGB", (int(widthRect), heightRect))
        # create rectangle image
        rectImageDraw = ImageDraw.Draw(rectImage)  
        rectImageDraw.rectangle(shape, fill ="white")
        # rectImage.show()
        # place the top image 
        rectImageMerge = rectImage
        # will need to use the following equation for landscape mode .... int((widthRect - widthTop) / 2)
        rectImageMerge.paste(topImage, (int((widthRect - widthTop) / 2), 0), topImage)
        rectImageMerge.show()
        # save the image as "screenshot_padding.png"
    else: 
        print('image is square enough')     
        # save the image as "screenshot_padding.png"

