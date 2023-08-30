# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:35:56 2023

@author: jgoncalves
"""
from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
#import tensorflow as tf
#import tensorflow_datasets as tfds
#import cv2 as cv
import os
import shutil
import os

import xlwings as xw
wb = xw.Book('C:/Users/jgoncalves/Desktop/scripts/CarBase - MO.xlsx')
sht = wb.sheets['Sheet1']
modelos = sht.range('E3:E652').value # assuming the column range is A2:A40
#print(modelos)


modelos_unique= []
for i in modelos:
    if i not in modelos_unique:
        modelos_unique.append(i)
#from tensorflow.keras import layers
print(modelos_unique)
path = r"D:\joaogonc\MODELOS_treino"
modelos = ['Citan','ClasseE','ClasseS','EQA','EQC','EQE','EQS','ForFour','ForTwo','GLA','GLA(156)','GLB','GLE','SL','Vito']

# for image in os.listdir('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents'):
#     lst = os.listdir('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents') # your directory path
#     number_files = len(lst)
#     print(number_files)
#     # img = cv.imread('D:\joaogonc\MODELOS_treino/{}/{}'.format(modelo,image), 0)
#     # rows, cols = img.shape
#     # M = np.float32([[1, 0, 0],
#     # 				[0, -1, rows],
#     # 				[0, 0, 1]])
#     # reflected_img = cv.warpPerspective(img, M,(int(cols),int(rows)))		
#     # cv.imwrite(image, reflected_img)

#     # grayscaled = tf.image.rgb_to_grayscale(image)
#     # cv.imwrite(image, grayscaled)
#     img = Image.open('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents/{}'.format(image))
#     rotated_image3 = img.rotate(60)
#     #rotated_image3.show()
#     rotated_image3.save('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents/rotated2_{}'.format(image))

for image in os.listdir('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents'):
    lst = os.listdir('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents') # your directory path
    number_files = len(lst)
    print(number_files)
    # img = cv.imread('D:\joaogonc\MODELOS_treino/{}/{}'.format(modelo,image), 0)
    # rows, cols = img.shape
    # M = np.float32([[1, 0, 0],
    # 				[0, -1, rows],
    # 				[0, 0, 1]])
    # reflected_img = cv.warpPerspective(img, M,(int(cols),int(rows)))		
    # cv.imwrite(image, reflected_img)

    # grayscaled = tf.image.rgb_to_grayscale(image)
    # cv.imwrite(image, grayscaled)
    
    #color_change
    #img = Image.open('D:\joaogonc\MODELOS_treino/GLC/{}'.format(image))
    img = Image.open('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents/{}'.format(image))
    # # Creating object of Sharpness class
    im3 = ImageEnhance.Color(img)
      
    # # showing resultant image
    im3.enhance(3.0).save('D:/joaogonc/scratch/Car Damage Detection For Scratch.v1i.multiclass/train/Severe-dents/contrast1_{}'.format(image))
    #im3.enhance(4.0).show()

    
    #ROTATE
    #rotated_image3 = img.rotate(-60)
    #rotated_image3.show()
    #rotated_image3.save('D:/joaogonc/MODELOS_treino/ClasseB/rotated2_{}'.format(image))


# for modelo in modelos_unique:
#     if os.path.isdir('D:\joaogonc\MODELOS_treino/{}'.format(modelo)):
#         for image in os.listdir('D:\joaogonc\MODELOS_treino/{}'.format(modelo)):
            
#             # print(image)
#             # img = cv.imread('D:\joaogonc\MODELOS_treino/{}/{}'.format(modelo,image), 0)
#             # rows, cols = img.shape
#             # M = np.float32([[1, 0, 0],
#             # 				[0, -1, rows],
#             # 				[0, 0, 1]])
#             # reflected_img = cv.warpPerspective(img, M,(int(cols),int(rows)))		
#             # cv.imwrite(image, reflected_img)

#             # grayscaled = tf.image.rgb_to_grayscale(image)
#             # cv.imwrite(image, grayscaled)
            
#             #color_change
#             img = Image.open('D:\joaogonc\MODELOS_treino/{}/{}'.format(modelo,image))
#             # Creating object of Sharpness class
#             im3 = ImageEnhance.Contrast(img)
              
#             # showing resultant image
#             im3.enhance(3.0).show()
            
            
# for dirs in os.walk(r"C:\Users\jgoncalves\Desktop\MODELOS2"):
#     for image in dirs:  
#         img = cv.imread(image, 0)
#         rows, cols = img.shape
#         M = np.float32([[1, 0, 0],
#         				[0, -1, rows],
#         				[0, 0, 1]])
#         reflected_img = cv.warpPerspective(img, M,
#         								(int(cols),
#         									int(rows)))
#         print(image)
#         cv.imwrite(image, reflected_img)
#         cv.waitKey(0)
#         cv.destroyAllWindows()
#         # grayscaled = tf.image.rgb_to_grayscale(image)
#         # cv.imwrite(image, grayscaled)
        