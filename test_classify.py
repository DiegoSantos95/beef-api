from tensorflow import keras
# Bibliotecas de ajuda
import numpy as np
from keras.models import load_model
import numpy as np
import argparse
import random
from PIL import Image
import keras
import tensorflow as tf
from array import *
import matplotlib.pyplot as plt


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to out input directory of images")
args = vars(ap.parse_args())

Im = Image.open(args["image"]).convert('L')
# plt.imshow(Im)
# plt.show()

pixel = Im.load()

width, height = Im.size
# print(width, height)
data_image = []
for x in range(0,width):
	for y in range(0,height):
		data_image.append(pixel[y, x] / 255.0)

data_image = np.array(data_image).reshape(1,96,96)
# plt.imshow(data_image[0,:,:])
# plt.show()

model = tf.keras.models.load_model('/Users/diego.santos/TCC-Anhembi/arroba-server/model2.h5')

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

pred = model.predict(data_image)
pred = pred.argmax(axis=1)[0]

if pred == 1:
	print ("Bovino pronto para o abate!")
	print ("predict =", pred)
elif pred == 0:
	print ("Bovino ainda não está pronto para o abate!")
	print ("predict =", pred)
else:
	print ("Não foi possível identificar!")