#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import tkinter 

#this function return file path
def open_file ():
    window = tkinter.Tk()
    window.withdraw()
    file = tkinter.filedialog.askopenfilename()
    return file


# In[3]:


#convert image to one dimension with row scaning
def Img2liste_row(img):    
    return img.reshape(img.shape[0]*img.shape[1])


# In[4]:


#convert image to one dimension with column scaning
def Img2liste_col(img):    
    return img.transpose().reshape(img.shape[1]*img.shape[0])


# In[5]:


#convert image to one dimension with zigzag scaning
def Img2liste_zigzag(img):
    if len(img)%2==0:
        variable=1
    else:
        variable=0
    return np.concatenate([np.flipud(img).diagonal(i) if i%2==variable else np.flipud(img).diagonal(i)[::-1]
                           for i in range(-len(img)+1,img.shape[1])])


# In[6]:


#choose the type of scan
def type_scan(image,scan):
    if scan=='Row':
        return np.concatenate([Img2liste_row(image[:,:,0]),Img2liste_row(image[:,:,1]),Img2liste_row(image[:,:,2])]) 
    elif scan=='Column':
        return np.concatenate([Img2liste_col(image[:,:,0]),Img2liste_col(image[:,:,1]),Img2liste_col(image[:,:,2])]) 
    else:
        return np.concatenate([Img2liste_zigzag(image[:,:,0]),Img2liste_zigzag(image[:,:,1]),Img2liste_zigzag(image[:,:,2])]) 


# In[7]:


#convert liste to 2 dimension with row scaning
def liste2img_row(serie,nl,nc):
    return np.reshape(serie, (nl, nc)).astype(int)


# In[8]:


#convert liste to 2 dimension with column scaning
def liste2img_col(serie,nl,nc):
    return np.reshape(serie, (nc, nl)).astype(int).transpose()


# In[9]:


import itertools

#convert liste of items into liste of blocks 
def liste2blocks (liste,nl,nc):
    
    l=[];k=0;j=0
    
    #boucle with chain function that combaine two ranges and repraet function
    for i in itertools.chain(range(1,min(nl,nc)),itertools.repeat(min(nl,nc),nc-nl+1),reversed(range(1,min(nl,nc)))):
        
        #determine interval of liste
        k=j;j+=i
        
        #append list with items in l list
        l.append(list(liste[k:j]))
        
    return [l[i][::-1] if i%2==1 else l[i] for i in range(len(l)) ]


# In[10]:


import itertools

#convert liste to 2 dimension with zigzag scaning
def liste2img_zigzag(mat,nl,nc):
    
    #creat matrix
    g=np.zeros((nl,nc))
    
    #convert liste of items into liste of blocks 
    matrix=liste2blocks (mat,nl,nc)
    
    #boucle with chain function that combaine two ranges
    for i in itertools.chain(range(-nl,0),range(1,nc)):
        
        #fill the negative diagonal (left half of matrix)
        if i<0:
            np.fill_diagonal(g[i:,:],matrix[-i-1])
            
        #fill the positive diagonal (right half of matrix)
        else:
            np.fill_diagonal(g[:,i:],matrix[i+nl-1])
            
    return np.flipud(g)


# In[11]:


#choose the type of scan reverse
def type_scan_reverse(data,scan,nl,nc):
    if scan=='Row':
        r=liste2img_row(data[0],nl,nc)
        g=liste2img_row(data[1],nl,nc)
        b=liste2img_row(data[2],nl,nc)
        return np.dstack((r,g,b))
    elif scan=='Column':
        r=liste2img_col(data[0],nl,nc)
        g=liste2img_col(data[1],nl,nc)
        b=liste2img_col(data[2],nl,nc)
        return np.dstack((r,g,b))
    else:
        r=liste2img_zigzag(data[0],nl,nc)
        g=liste2img_zigzag(data[1],nl,nc)
        b=liste2img_zigzag(data[2],nl,nc)
        return np.dstack((r,g,b))


# In[12]:


from random import randint

#generate binary matrix
def gen_mat_bin(nl,nc):
    liste=[randint(0,1) for i in range(nl*nc) ]
    return np.array(liste).reshape(nl,nc)


# In[13]:


from random import randint

#generate gray matrix
def gen_mat_gray(nl,nc):
    liste=[randint(0,255) for i in range(nl*nc) ]
    return np.array(liste).reshape(nl,nc)


# In[14]:


#3d image to 1d image
def rgb2gray(I):
    return np.dot(I,[0.299, 0.5870, 0.1140])


# In[15]:


#this function divide a string of bits into blocks of 8 bits string 
def bin2dec(suit):
    return [suit[i:i+8] for i in range(0,len(suit),8)] 


# In[16]:


#write data in texte file
def one(liste):
    
    #converts liste of 8 bits into carateres
    caractere=[chr(int(i,2)) for i in liste]
    
    #create a texte file  
    file = open(input("file name : ")+".txt", 'w')
    for i in caractere:
        file.write(i)
    file.close()
    
    return 'Fichier a ete creer'


# In[17]:


import matplotlib.pyplot as plt 

#write data in image file
def two(liste,params):
    
    #converts liste of 8 bits into pixels values
    pixels=[int(i,2) for i in liste]
    
    #call liste2img_row function
    image=liste2img_row(pixels,params[0],params[1])
    
    return plt.imshow(image,cmap=plt.get_cmap('gray'))


# In[18]:


import wave
import sounddevice as sd

#write data in audio file
def three(liste,params):
    
    ##converts liste of 8 bits into ascci values
    data_ori=[int(i,2) for i in liste]
    
    #the next 3 lines are for create audio file 
    #audio=wave.open(input("Audio name : ")+".wav","w")
    #audio.setparams((params[0],params[1],params[2],params[3],params[4],params[5]))
    #audio.writeframes(np.frombuffer(bytes(data_ori),np.dtype(int)))
    
    return sd.play(np.frombuffer(bytes(data_ori),np.dtype(int)) , params)


# In[19]:


#take come input liste o repetition and return a liste of tuples of symbol(0/1) and repetition
def tupl(liste):
    
    #if the liste start with 0 that means the first number is repetition of 0 
    if liste[0]==0:
        liste.pop(0)
        n=0;m=1
    
    #vice vesa
    else:
        n=1;m=0
        
    return[(liste[i],n) if i%2==0 else (liste[i],m) for i in range(len(liste))]


# In[20]:


#return a dictionary of symbol and frequance
def frequance(seq):
    return dict((i,seq.count(i)) for i in set(seq))


# In[21]:


from PIL import Image

#calculate size of matrix image
def size_original(image):
    
    #extract parameters
    params=[image.size[0],image.size[1],image.mode]
    
    #for image index
    if params[2]=='1':
        return params[0]*params[1]*(10**-3)
    
    #for any other systeme-color
    else:
        return params[0]*params[1]*len(params[2])*8*(10**-3)


# In[22]:


from PIL import Image
import os

#change image format
def save_image(image,path,formate):
    filename=os.path.splitext(path)[0]+f".{formate}"
    image.save(filename)
    return filename


# In[23]:


from tkinter import *

#create labels
def creat_label(frame,number,title,start):
    y=start
    for i in range(number):
        Label(frame, text=title[i],font=("",10),bg='#003049',fg='white').place(relx=.2, rely=y,anchor= CENTER,
                                                                               relheight=0.05, relwidth=0.4)
        y+=0.1


# In[24]:


from tkinter import *

#create entries
def creat_entry(frame,number,start,params,State):
    y=start
    for i in range(number):
        e=Entry(frame,state=State)
        e.insert(0,params[i])
        e.place(relx=.6, rely=y,anchor= CENTER,relheight=0.05, relwidth=0.4)
        y+=0.1


# In[ ]:




