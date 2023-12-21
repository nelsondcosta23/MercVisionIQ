# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 22:24:28 2023

@author: joaog
"""

import cv2
import numpy as np
import tensorflow as tf
import os
import csv
import math
import operator
import time

import shutil        
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import requests

from sklearn.cluster import KMeans
from skimage import io
import matplotlib.pyplot as plt
import argparse
import webcolors

import PIL
from PIL import Image, ImageTk 

from pandas import ExcelWriter, DataFrame
import pandas as pf
import pyforms
from   pyforms          import BaseWidget
from   pyforms.controls import ControlText
from   pyforms.controls import ControlButton
from tkinter import *
#from tkinter.ttk import *
from tkinter import filedialog, messagebox, PhotoImage, Label, ttk
from tkinter.filedialog import askopenfilename,askdirectory


class window(): 
    def __init__(self):
        self.root = Tk()
        self.catalogo = "https://workplace2.soccsantos.cloud/upload/foto_bonita/"
        self.save_file_path = "./Imagens a Cortar/"
        self.excel_path = "./Registo_Catalogo.xlsx"
        self.folder_path_fotos = "./Fotos/"
        self.excel_cortar_path = "./Imagens_a_Cortar.xlsx"
        self.path_modeloModelo = "./mercvision17_0.94175.h5"
        self.path_modeloModelo_pesos = "./mercvision_pesos_sg17.hdf5"
        self.path_modeloCor = "./color_model.h5"
        self.logo = "./logo.png"
        self.temp_folder = "./website_temp"
        ############## gif

        ###########
        self.status = str()
        self.path_foto = str()
        self.matricula = []
        self.modelo_1 = str()
        self.cor_1 = str()
        self.matricula_rec = str()
        self.l1 = []
        self.path_ = str()
        self.modelo = []
        self.cor = []
        self.form()
        self.root.mainloop()

#Classificação de Cor
########################################################################################################################
########################################################################################################################
    
    def CNN(self,path):
        # Previsão através de uma imagem
        #definir tamanho das imagens
        nlinhas = 256
        ncolunas = 256
        canais = 3  #dimensões das cores (1 para preto e branco e 3 para colorido)
        image = cv2.imread(path)
        
        #### Marca
        model_modelo = tf.keras.models.load_model(self.path_modeloModelo)
        model_modelo.load_weights(self.path_modeloModelo_pesos)
        imagem_1 = cv2.resize(image, (nlinhas,ncolunas), interpolation=cv2.INTER_CUBIC)
        imagem_1 = tf.expand_dims(np.array(imagem_1).astype("float32") / 255, 0)   
        pred_modelo = model_modelo.predict(imagem_1)
        pred_modelo = np.argmax(pred_modelo)
        marcas = ['Citan','CLA','ClasseA','ClasseB','ClasseC(205)','ClasseC(206)','ClasseE','ClasseS','CLS','EQA','EQB','EQC','EQE','EQS','ForFour Novo','ForTwo Novo','ForFour','ForTwo','GLA(156)','GLA','GLB','GLC','GLE','SL','Vito']
        #### Cor
        model_cor = tf.keras.models.load_model(self.path_modeloCor)
        tipo_img = path.split(".")[1]
        
        if tipo_img == "jpg" or "jpeg":
            y=600
            x=600
            h=200
            w=1000
        elif tipo_img == "png":
            y=500
            x=600
            h=200
            w=750
           
        crop_img=image[y:y+h,x:x+w]
        imagem_2 = cv2.resize(crop_img, (nlinhas,ncolunas), interpolation=cv2.INTER_CUBIC)
        imagem_2 = tf.expand_dims(np.array(imagem_2).astype("float32") / 255, 0)   
        pred_cor = model_cor.predict(imagem_2)
        pred_cor = np.argmax(pred_cor)
        cores = ['azul','azul_escuro','branco','cinzento claro','cinzento escuro','laranja','preto','vermelho','castanho']
        
        #crop_img = self.increase_brightness(crop_img)
        
        
        # show our image
        plt.figure()
        plt.axis("off")
        plt.imshow(image)
        
        
        # reshape the image to be a list of pixels
        #crop_img = crop_img.reshape((crop_img.shape[0] * crop_img.shape[1], 3))
        # cluster the pixel intensities
        #clt = KMeans(n_clusters =3)
        #clt.fit(crop_img)
    
        # build a histogram of clusters and then create a figure representing the number of pixels labeled to each color
        #hist = self.centroid_histogram(clt)
       # bar, max_colour = self.plot_colors(hist, clt.cluster_centers_)
    
    
        return marcas[pred_modelo],cores[pred_cor]        #max_colour[1]

    def show_img(self):
        load = PIL.Image.open(self.path_foto)
        width, height = load.size 
        newsize = (400, 300)
        load = load.resize(newsize)
        render = ImageTk.PhotoImage(load)
        img = Label(self.root,image = render)
        img.image = render
        img.grid(row = 1, column = 1)
    
    def imagem_in_dir(self):
        self.modelo_1, self.cor_1 = self.CNN(self.path_foto)
        self.matricula_rec = ""
        #self.cor_1 = self.colors_pt(self.cor_1)
        #print(self.modelo_1, self.cor_1)
        #print(self.modelo)
        for i in range(len(self.modelo)):
            if (self.modelo[i],self.cor[i]) == (self.modelo_1,self.cor_1):
                self.matricula_rec = self.matricula[i]

        if [self.modelo_1,self.cor_1] not in self.l1:
            self.status = 'A viatura {} de cor {} NÃO está no catálogo\nSe quiser colocar no catálogo, deve "Enviar Mail Nelson"\nSenão apenas passar à próxima imagem'.format(self.modelo_1,self.cor_1)
            print(self.path_foto,self.save_file_path)
        else:
            self.status = 'A viatura {} de cor {} está no catálogo\nSe quiser colocar no catálogo, deve "Enviar Mail Nelson"\nSe quiser a foto sem fundo clicar "Enviar Mail Recortada"\nSenão apenas passar à próxima imagem'.format(self.modelo_1,self.cor_1)

    def imagem_in_dir_automatico(self):
        dir_=os.listdir(self.folder_path_fotos)
        for imagem in dir_:
            modelo_1, cor_1 = self.CNN(self.folder_path_fotos + "/" + imagem)
            #cor_1 = self.colors_pt(cor_1)
            #print(modelo_1,cor_1)
            imagem = imagem.split('.')[0]
            #self.matricula_n_unique.append(imagem)
            #self.cor_n_unique.append(cor_1)
            #self.modelo_n_unique.append(modelo_1)
            if [modelo_1,cor_1] not in self.l1:
                self.l1.append([modelo_1,cor_1])
                self.modelo.append(modelo_1)
                self.cor.append(cor_1)
                self.matricula.append(imagem)
                shutil.copy(self.folder_path_fotos + imagem + '.JPG',self.save_file_path)
                print(self.folder_path_fotos + imagem + '.JPG',self.save_file_path)
                
    def write_excel(self):
        df = DataFrame({'nome ficheiro':self.matricula, 'modelo':self.modelo, 'cor':self.cor})
        print(self.matricula)
        with ExcelWriter(self.excel_cortar_path) as writer:  
            df.to_excel(writer, sheet_name='Sheet1')
 

    def focus1(self,event):
        # set focus on the course_field box
        self.path_field_foto.delete(0,END)
        self.path_foto = filedialog.askopenfilename()
        self.path_foto = str(self.path_foto)
        self.path_field_foto.insert(0,self.path_foto)
        print(self.path_foto)
 

    def focus4(self,event):
        self.l1 = []
        self.read_excel(self.excel_path)
        try:
            self.bar()
            self.imagem_in_dir()
            

        
            #self.progress['value'] = 100
            self.show_img()
            self.text.delete('1.0',END)
            self.text.insert('1.0',self.status)
            self.progress['value'] = 0
        except:
            messagebox.showwarning(title="Aviso", message="Não foi selecionada uma foto compatível")
            self.progress['value'] = 0
            
            
        
        #self.write_excel()
        
    def bar(self):
        for i in range(90):
            self.progress['value'] = i
            self.root.update_idletasks()  # Update the Tkinter window
            self.root.after(5) 
    
    def read_excel(self,path):
        import pandas as pd 
        df = pd.read_excel(path)
        self.matricula = df["matrículas"].tolist()
        self.modelo = df["modelo"].tolist()
        self.cor = df["cor"].tolist()
        for i in range(len(self.modelo)):
            self.l1.append([self.modelo[i],self.cor[i]])
        #print(self.l1,self.modelo,self.matricula,self.cor)

    def focus6(self,event):
        self.imagem_in_dir_automatico()
        self.write_excel()
        self.env_mail_zip()

    def env_mail_rec(self,event):
       # try:
            email_sender = "testingsoccsantos@gmail.com"
            email_password = "gggy hzdn dibs ttev"
            email_receiver = "joao.g.oncalves@hotmail.com"
            
            subject = "MercVision"
            body = "Cortadas ({},{})".format(self.modelo_1,self.cor_1)
            
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            em.add_alternative(body, subtype='html')
    
            print(self.catalogo)
            l1 = self.matricula_rec.split("-")
            self.matricula_rec = ""
            for i in l1:
                self.matricula_rec += i
                print(i)
            # Attach the image file
            url = self.catalogo + self.matricula_rec + ".png"
            print(url)
            ### antigo ir buscar a pasta catalogo
            #with open(str(self.catalogo + self.matricula_rec + '.png'), 'rb') as attachment_file:
            #    file_data = attachment_file.read()
            #    file_name = attachment_file.name.split("/")[-1]
            
            #ir buscar ao site
            save_folder = self.temp_folder
            filename = "foto.png"

            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if the request was successful
        
                os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist
        
                save_path = os.path.join(save_folder, filename)
                with open(save_path, 'wb') as file:
                    file.write(response.content)
        
                print(f"Image downloaded successfully and saved to {save_path}")
        
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
            
            # Example usage:
            #image_url = url
            #save_path = 'downloaded_image.jpg'

            with open(self.temp_folder + "/foto.png", 'rb') as attachment_file:
                file_data = attachment_file.read()
                file_name = attachment_file.name.split("/")[-1]
            
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
            em.attach(attachment)
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
                
            try:
                os.remove(self.temp_folder + "foto.png")
                print(f"{file_path} deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
            
            messagebox.showwarning(title="Aviso", message="Email com a foto recortada ENVIADO!")
            
        #except:
         #   messagebox.showwarning(title="Aviso", message="Não há foto recortada disponível para envio")
        
        
        
    def env_mail_zip(self):
        email_sender = "testingsoccsantos@gmail.com"
        email_password = "gggy hzdn dibs ttev"
        email_receiver = "joao.g.oncalves@hotmail.com"
        
        subject = "MercVision"
        body = "Olhá Pasta".format(self.modelo_1, self.cor_1)
        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        em.add_alternative(body, subtype='html')

        source_excel_file = self.excel_cortar_path
        destination_folder = self.save_file_path
        
        try:
            # Use shutil.copy to copy the file to the folder
            shutil.copy(source_excel_file, destination_folder)
    
        
            print(f"Excel file moved to {destination_folder}")
        except Exception as e:
            print(f"Error: {e}")
                
        # Zip the folder
        folder_to_zip = self.save_file_path  # Replace with the path to the folder you want to zip
        zip_file_name = "attachment.zip"
        
        with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_to_zip):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_to_zip))
        
        # Attach the zipped folder
        with open(zip_file_name, 'rb') as attachment_file:
            file_data = attachment_file.read()
            attachment = MIMEBase('application', 'zip')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{zip_file_name}"')
            em.attach(attachment)
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        # Remove the temporary zip file
        os.remove(zip_file_name)
        
        messagebox.showwarning(title="Aviso", message="Email com as fotos com destino ao catálogo ENVIADO!")


    def env_mail(self,event):

        email_sender = "testingsoccsantos@gmail.com"
        email_password = "gggy hzdn dibs ttev"
        email_receiver = "joao.g.oncalves@hotmail.com"
        
        subject = "MercVision"
        body = "É pra cortar ({},{})".format(self.modelo_1,self.cor_1)
        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        em.add_alternative(body, subtype='html')
        
        # Attach the image file
        with open(self.path_foto, 'rb') as attachment_file:
            file_data = attachment_file.read()
            file_name = attachment_file.name.split("/")[-1]
        
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
        em.attach(attachment)
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
            
        messagebox.showwarning(title="Aviso", message="Email com a foto a adicionar ao catálogo ENVIADA!")

           
    
    def form(self):
        self.root.configure(background='midnight blue')
        self.root.title("MercVision")
        self.root.geometry("1100x600")
        
        size = (300,100)
        userImage = PIL.Image.open(self.logo)
        userImage = userImage.resize(size)
        self.img = ImageTk.PhotoImage(userImage)
        self.label = Label(self.root,image = self.img)
        self.label.grid(row = 0,column = 0)
        
        self.path = Button(self.root,text='Escolher Foto',bg='white',padx = 50)
        self.path.bind("<Button>",self.focus1)
        self.path.grid(row = 1, column = 0,sticky = N,padx = 20,pady = 20)
        self.path_field_foto = Entry(self.root, textvariable = self.path_foto) 
        self.path_field_foto.bind("<Button>",self.focus1)
        self.path_field_foto.grid(row=0,column=1,ipadx='250',sticky = N,padx = 10,pady = 20)

        
        self.button3 = Button(self.root,text = 'Verificar Catálogo',fg = 'Black',bg='Grey')
        self.button3.bind('<Button>',self.focus4)
        self.button3.grid(row=4, column=0)

        self.button4 = Button(self.root,text = 'Enviar Mail Único',fg = 'Black',bg='Grey')
        self.button4.bind('<Button>',self.env_mail)
        self.button4.grid(ipadx='50',row=4, column=1,sticky = W,padx = 250)

        self.button5 = Button(self.root,text = 'Enviar Mail Todas as Fotos',fg = 'Black',bg='Grey')
        self.button5.bind('<Button>',self.focus6)
        self.button5.grid(ipadx='27',row=5, column=1,sticky = W,padx = 250)

        self.button6 = Button(self.root,text = 'Enviar Mail Recortada',fg = 'Black',bg='Grey')
        self.button6.bind('<Button>',self.env_mail_rec)
        self.button6.grid(ipadx='39',row=6, column=1,sticky = W,padx = 250)

        self.text = Text(self.root,height = 5)
        self.text.grid(row = 7,column = 1)
        self.text.insert('1.0',"Escolher Foto e Verificar Catálogo\n")
        self.text.insert('2.0',"Enviar Mail Todas as Fotos -  Processa todas as Fotos e envia numa pasta zipada")
        
        #self.progress = Label(self.root,image = "")
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=250, mode='determinate')
        self.progress.grid(row = 5,column = 0)

    
if __name__ == '__main__':
    win = window()
    #env_mail_zip()

    

    

    
