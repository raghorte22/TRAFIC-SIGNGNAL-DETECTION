#!/usr/bin/env python
# coding: utf-8

# ### trafic signal

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
import os
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D,MaxPool2D,Dense,Flatten,Dropout

data=[]
labels=[]
classes=43
cur_path =os.getcwd()

for i in range(classes):
    path = os.path.join(cur_path, "E:\\resume projects\\trafic\\Train", str(i))

    images=os.listdir(path)
    
    for a in images:
        try:
            image=Image.open(path +'\\'+a)
            image=image.resize((30,30))
            image =np.array(image)
            data.append(image)
            labels.append(i)
        except:
            print("Error loading image")
data= np.array(data)
labels =np.array(labels)
            
        


# In[2]:


print(data.shape ,labels.shape)
x_train,x_test,y_train,y_test=train_test_split(data,labels,test_size=0.2,random_state=42)

print(x_train.shape ,x_test.shape,y_train.shape,y_test.shape)

y_train = to_categorical(y_train , 43)
y_test = to_categorical(y_test,43)


# In[3]:


model= Sequential()
model.add(Conv2D(filters=32 ,kernel_size=(5,5),activation='relu' ,input_shape=x_train.shape[1:]))
model.add(Conv2D(filters=32 ,kernel_size=(5,5) ,activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(rate=0.25))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation='relu'))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(43,activation='softmax'))

#compilation of the model
model.compile(loss='categorical_crossentropy' ,optimizer='adam' ,metrics=['accuracy'])



# ### step 3: TRAIN AND VALIDATE THE MODEL

# In[4]:


epochs =15
history =model.fit(x_train,y_train ,batch_size=64,epochs=epochs ,validation_data=(x_test ,y_test))


# In[5]:


model.save("my_model.h5")


# In[6]:


#testing accuracy an test dataset

from sklearn.metrics import accuracy_score

y_test = pd.read_csv(r"E:\\resume projects\\trafic\\Test.csv")
                     
labels = y_test["ClassId"].values
imgs = y_test["Path"].values
                     
data=[]
for img in imgs:
    print(img)
    image = Image.open(img)
    image = image.resize((30,30))  
    data.append(np.array(image))                 


# In[7]:


plt.figure(0)
plt.plot(history.history['accuracy'],label='training accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.title('Accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()



plt.figure(1)
plt.plot(history.history['loss'] ,label='training loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()


# ### STEP 4: TEST OUR MODEL WITH TEST DATASET

# In[8]:


from sklearn.metrics import accuracy_score
import pandas as pd
from PIL import Image
import numpy as np

# Assuming you have already loaded and compiled your model
# model = ...

y_test = pd.read_csv("E:\\resume projects\\trafic\\Test.csv")

labels = y_test["ClassId"].values
imgs = y_test["Path"].values

data = []

for img in imgs:
    image = Image.open(img)
    image = image.resize((30, 30))
    data.append(np.array(image))

x_test = np.array(data)

# Use predict method to get the probabilities for each class
pred_probabilities = model.predict(x_test)

# Use argmax to get the predicted class
pred = np.argmax(pred_probabilities, axis=1)

# Accuracy with the test data
accuracy = accuracy_score(labels, pred)
print("Accuracy:", accuracy)


# #In the end, we are going to save the model that we have trained using the Keras model.save() function.

# In[9]:


model.save('traffic_classifier.h5')


# In[13]:


import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

import numpy
#load the trained model to classify sign
from keras.models import load_model
model = load_model('traffic_classifier.h5')
#dictionary to label all traffic signs class.
classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)', 
            3:'Speed limit (50km/h)', 
            4:'Speed limit (60km/h)', 
            5:'Speed limit (70km/h)', 
            6:'Speed limit (80km/h)', 
            7:'End of speed limit (80km/h)', 
            8:'Speed limit (100km/h)', 
            9:'Speed limit (120km/h)', 
            10:'No passing', 
            11:'No passing veh over 3.5 tons', 
            12:'Right-of-way at intersection', 
            13:'Priority road', 
            14:'Yield', 
            15:'Stop', 
            16:'No vehicles', 
            17:'Veh > 3.5 tons prohibited', 
            18:'No entry', 
            19:'General caution', 
            20:'Dangerous curve left', 
            21:'Dangerous curve right', 
            22:'Double curve', 
            23:'Bumpy road', 
            24:'Slippery road', 
            25:'Road narrows on the right', 
            26:'Road work', 
            27:'Traffic signals', 
            28:'Pedestrians', 
            29:'Children crossing', 
            30:'Bicycles crossing', 
            31:'Beware of ice/snow',
            32:'Wild animals crossing', 
            33:'End speed + passing limits', 
            34:'Turn right ahead', 
            35:'Turn left ahead', 
            36:'Ahead only', 
            37:'Go straight or right', 
            38:'Go straight or left', 
            39:'Keep right', 
            40:'Keep left', 
            41:'Roundabout mandatory', 
            42:'End of no passing', 
            43:'End no passing veh > 3.5 tons' }


# In[14]:


def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30,30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)
    pred = model.predict(image)[0]  # Use model.predict instead of predict_generator
    pred_class = np.argmax(pred) + 1  # Get the index of the maximum value
    sign = classes[pred_class]
    print(sign)
    label.configure(foreground='#011638', text=sign)


# In[15]:


import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
#initialise GUI
top=tk.Tk()
top.geometry('800x600')
top.title('Traffic sign classification')
top.configure(background='#CDCDCD')
label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
sign_image = Label(top)
def classify(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30,30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)

    pred = model.predict([image])
    pred_c = numpy.argmax(pred)+1
    sign = classes[pred_c]
    print(sign)
    label.configure(foreground='#011638', text=sign) 
def show_classify_button(file_path):
    classify_b=Button(top,text="Classify Image",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    classify_b.place(relx=0.79,rely=0.46)
def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_classify_button(file_path)
    except:  
        
         pass
upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
upload.pack(side=BOTTOM,pady=50)
sign_image.pack(side=BOTTOM,expand=True)
label.pack(side=BOTTOM,expand=True)
heading = Label(top, text="Know Your Traffic Sign",pady=20, font=('arial',20,'bold'))
heading.configure(background='#CDCDCD',foreground='#364156')
heading.pack()
top.mainloop()


# In[ ]:




