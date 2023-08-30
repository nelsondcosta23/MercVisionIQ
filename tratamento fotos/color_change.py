# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 17:20:40 2023

@author: jgoncalves

"""
from PIL import Image, ImageEnhance
 
 
img = Image.open(r"C:\Users\jgoncalves\Desktop\MODELOS_treino\ClasseC(206)\img_0_0_1754.jpg")
#img = img.convert("RGB")
 
#d = img.getdata()
 
#new_image = []
# for item in d:
 
#     # change all white (also shades of whites)
#     # pixels to yellow
#     if item[0] in list(range(175, 250)):
#         new_image.append((254, 100, 200))
#     else:
#         new_image.append(item)

#im3 = ImageEnhance.Brightness(img)
  
# # showing resultant image
#im3.enhance(2.0).show()
 
# save new image
#img.show()

# Creating object of Sharpness class
# im3 = ImageEnhance.Sharpness(img)
  
# # showing resultant image
# im3.enhance(-5.0).show()

# Creating object of Sharpness class
im3 = ImageEnhance.Contrast(img)
  
# showing resultant image
im3.enhance(3.0).show()