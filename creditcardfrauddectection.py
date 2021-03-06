import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.layers import Conv1D, MaxPool1D
from tensorflow.keras.optimizers import Adam

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('creditcard.csv')
data.head()

data.shape

data.isnull().sum()

data.info()

data['Class'].value_counts()

"""### Balance Dataset"""

non_fraud = data[data['Class']==0]
fraud = data[data['Class']==1]

non_fraud.shape, fraud.shape

non_fraud = non_fraud.sample(fraud.shape[0])
non_fraud.shape

data = fraud.append(non_fraud, ignore_index=True)
data

data['Class'].value_counts()

X = data.drop("Class", axis = 1)
y = data['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y)

X_train.shape, X_test.shape

# Avoids overfitting
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

X_train.shape

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

X_train.shape, X_test.shape

"""# Building the CNN"""

epochs = 20
model = Sequential()
# First Layer
model.add(Conv1D(32, 2, activation="relu", input_shape = X_train[0].shape))
model.add(BatchNormalization())
model.add(Dropout(0.2))

# Second Layer
model.add(Conv1D(64, 2, activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# Third Layer
model.add(Flatten())
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))

# Output Layer 
model.add(Dense(1, activation="sigmoid"))

model.summary()

model.compile(optimizer=Adam(lr=0.0001), loss = "binary_crossentropy", metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test), verbose=1)

def plot_learningCurve(history, epoch):
  # Plot training & validation accuracy values
  epoch_range = range(1, epoch + 1)
  plt.plot(epoch_range, history.history['accuracy'])
  plt.plot(epoch_range, history.history['val_accuracy'])
  plt.title('Model accuracy')
  plt.xlabel('Epoch')
  plt.ylabel('Accuracy')
  plt.legend(['Train', 'Val'], loc='upper left')
  plt.show()

  # Plot training & validation loss values
  plt.plot(epoch_range, history.history['loss'])
  plt.plot(epoch_range, history.history['val_loss'])
  plt.title('Model loss')
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.legend(['Train', 'Val'], loc='upper left')
  plt.show()

plot_learningCurve(history, epochs)

"""# Adding MaxPool"""

epochs = 50
model = Sequential()
# First Layer
model.add(Conv1D(32, 2, activation="relu", input_shape = X_train[0].shape))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.2))

# Second Layer
model.add(Conv1D(64, 2, activation="relu"))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.5))

# Third Layer
model.add(Flatten())
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))

# Output Layer 
model.add(Dense(1, activation="sigmoid"))

model.compile(optimizer=Adam(lr=0.0001), loss = "binary_crossentropy", metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test), verbose=1)
plot_learningCurve(history, epochs)
