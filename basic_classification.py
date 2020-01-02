from __future__ import absolute_import, division, print_function, unicode_literals, unicode_literals

# TensorFlow e tf.keras
import tensorflow as tf
from tensorflow import keras
# Bibliotecas de ajuda
import numpy as np
import matplotlib.pyplot as plt

# read CSV file with Training Images and Labels
csv_train_images = []
with open('train-images.csv', 'r') as filehandle:  
    csv_train_images = [current_place.rstrip() for current_place in filehandle.readlines()]

train_images = np.array(csv_train_images, dtype=float).reshape(354,96,96)
# plt.imshow(train_images[0,:,:])
# plt.show()

csv_train_labels = []
with open('train-labels.csv', 'r') as filehandle:       
    csv_train_labels = [current_place.rstrip() for current_place in filehandle.readlines()]

train_labels = np.array(csv_train_labels, dtype=int)

# read CSV file with Testing Images and Labels
csv_test_images = []
with open('test-images.csv', 'r') as filehandle:  
    csv_test_images = [current_place.rstrip() for current_place in filehandle.readlines()]

test_images = np.array(csv_test_images, dtype=float).reshape(62,96,96)
# plt.imshow(test_images[0,:,:])
# plt.show()

csv_test_labels = []
with open('test-labels.csv', 'r') as filehandle:       
    csv_test_labels = [current_place.rstrip() for current_place in filehandle.readlines()]

test_labels = np.array(csv_test_labels, dtype=int)

class_names = ['Não está Pronto', 'Pronto para o abate']

print(train_images.shape)

print(len(train_labels))

print (train_labels)

print (test_images.shape)

print (len(test_labels))

print (test_labels)

train_images = train_images / 255.0

test_images = test_images / 255.0

# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[train_labels[i]])
# plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(96,96)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(32, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, validation_split=0.15, epochs=90, batch_size=40, verbose=1)

with open('treino-dados.txt', mode='wt', encoding='utf-8') as file:
		file.write('\n'.join(str(line) for line in history.history['acc']))

with open('test-dados.txt', mode='wt', encoding='utf-8') as file:
		file.write('\n'.join(str(line) for line in history.history['val_acc']))

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

model.save('model_test.h5')

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:','%.2f' % (test_acc * 100),'%')

