# -*- coding: utf-8 -*-
"""derma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AOZKAaclSFjdqhinyHSOqPWlgcBXoJoV

# Import Libraries
"""

!pip install tensorflow

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import save_model, load_model
import tensorflow as tf

"""# Data Collcetion"""

from google.colab import drive
drive.mount('/content/drive')

"""# Data Pre-processing"""

# Data augmentation training
train_datagen = ImageDataGenerator(
    rescale=1./255,

    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Data augmentation testing
test_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Load and preprocess your custom dataset using ImageDataGenerator
train_set = train_datagen.flow_from_directory(
    '/content/drive/MyDrive/DermaAnalysis/Dataset/train',
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical'
)

test_set = train_datagen.flow_from_directory(
    '/content/drive/MyDrive/DermaAnalysis/Dataset/test',
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical'
)

"""# Model Implementation(VGG)"""

# Create a VGG-16 model with pre-trained weights from ImageNet

model_vgg = tf.keras.applications.VGG16(
    include_top=True,
    weights="imagenet",
    input_shape=(224,224,3),
    classifier_activation="softmax",
)

# Print model summary

model_vgg.summary()

# Freeze the pre-trained layers so they won't be updated during training
for layer in model_vgg.layers:
    layer.trainable = False

"""# Model Implementation(ResNet)"""

# Create a ResNet-50 model with pre-trained weights from ImageNet
model_resnet=tf.keras.applications.ResNet50(
    include_top=True,
    weights="imagenet",
    input_shape=(224,224,3),
)

# Print model summary

model_resnet.summary()

# Freeze the pre-trained layers so they won't be updated during training
for layer in model_resnet.layers:
    layer.trainable = False

"""# Model Implementation(MobileNet)"""

# Create a MobileNet model with pre-trained weights from ImageNet
model_mobilenet=tf.keras.applications.MobileNet(
    input_shape=(224,224,3),
    include_top=True,
    weights="imagenet",
    classifier_activation="softmax",
)

# Print the model summary
model_mobilenet.summary()

# Freeze the pre-trained layers so they won't be updated during training
for layer in model_mobilenet.layers:
    layer.trainable = False

"""# Load Model"""

# Create a new model by adding custom layers for your classification task
model__vgg = Sequential()
model__vgg.add(model_vgg)
model__vgg.add(Flatten())
model__vgg.add(Dense(128, activation='relu'))
model__vgg.add(Dropout(0.5))
model__vgg.add(Dense(19, activation='softmax'))

# Create a new model by adding custom layers for your classification task
model__res = Sequential()
model__res.add(model_resnet)
model__res.add(Flatten())
model__res.add(Dense(128, activation='relu'))
model__res.add(Dropout(0.5))
model__res.add(Dense(19, activation='softmax'))

# Create a new model by adding custom layers for your classification task
model__mob = Sequential()
model__mob.add(model_mobilenet)
model__mob.add(Flatten())
model__mob.add(Dense(128, activation='relu'))
model__mob.add(Dropout(0.5))
model__mob.add(Dense(23, activation='softmax'))

# Compile the model
model__vgg.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Compile the model
model__res.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Compile the model
model__mob.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# fit the model
model__res.fit(
    train_set,
    steps_per_epoch=len(train_set),
    epochs=2,
    validation_data=test_set,
    validation_steps=len(test_set)
)

"""# Model Tuning"""

import os

# Directory where your dataset is stored
dataset_dir = '/content/drive/MyDrive/DermaAnalysis/Dataset/test'

# Get the class names (which are the directory names in the dataset directory)
class_names = sorted(os.listdir(dataset_dir))

print("Class names:", class_names)



"""# Save Model"""

# Save the entire  Resnet model (architecture, weights, and training configuration)
model__res.save('model_ResNet.h5')

# Save the entire  Resnet model (architecture, weights, and training configuration)
model__res.save('model_ResNet.h5')

# Save the entire Vgg model (architecture, weights, and training configuration)
model__vgg.save('/content/drive/MyDrive/DermaAnalysis/Dataset/model_VGG.h5')

# Save the entire Mobilenet model (architecture, weights, and training configuration)
model__mob.save('/content/drive/MyDrive/DermaAnalysis/Dataset/model_MobileNet.h5')

# Load your Keras model (replace 'model.h5' with the path to your Keras model)
model = tf.keras.models.load_model('model_ResNet.h5')

# Convert the Keras model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("/content/drive/MyDrive/DermaAnalysis/model_ResNet.tflite", 'wb') as f:
    f.write(tflite_model)

"""# Testing / Implementation"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the saved model
model = load_model('model_ResNet.h5')

# Load and preprocess a single input image
img_path = 'car 3.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Get predictions for the input image
predictions = model.predict(img_array)

# Customize this based on your dataset's classes
class_labels = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Atopic Dermatitis Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']

# Get the predicted class index
predicted_class_index = np.argmax(predictions, axis=1)[0]

# Get the predicted class label
predicted_class_label = class_labels[predicted_class_index]

# Display the input image and predicted class label
plt.imshow(img)
plt.axis('off')
plt.title(f'Predicted Class: {predicted_class_label}')
plt.show()

+import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the saved model
model = load_model('model_ResNet.h5')

# Load and preprocess a single input image
img_path = 'image 1.jpeg'
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Get predictions for the input image
predictions = model.predict(img_array)

# Customize this based on your dataset's classes
class_labels = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Atopic Dermatitis Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']

# Get the predicted class index
predicted_class_index = np.argmax(predictions, axis=1)[0]

# Get the predicted class label
predicted_class_label = class_labels[predicted_class_index]

# Display the input image and predicted class label
plt.imshow(img)
plt.axis('off')
plt.title(f'Predicted Class: {predicted_class_label}')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load the saved model
model = load_model('model_ResNet.h5')

# Load and preprocess a single input image
img_path = 'qqq.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Get predictions for the input image
predictions = model.predict(img_array)

# Customize this based on your dataset's classes
class_labels = ['Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 'Atopic Dermatitis Photos', 'Cellulitis Impetigo and other Bacterial Infections', 'Eczema Photos', 'Exanthems and Drug Eruptions', 'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 'Poison Ivy Photos and other Contact Dermatitis', 'Psoriasis pictures Lichen Planus and related diseases', 'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections']

# Get the predicted class index
predicted_class_index = np.argmax(predictions, axis=1)[0]

# Get the predicted class label
predicted_class_label = class_labels[predicted_class_index]

# Display the input image and predicted class label
plt.imshow(img)
plt.axis('off')
plt.title(f'Predicted Class: {predicted_class_label}')
plt.show()

"""# Evaluation"""











"""# Plotting"""

print("hello world ")







