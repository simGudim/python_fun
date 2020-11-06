import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
from keras.models import model_from_json
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler 
from matplotlib import pyplot as plt
from keras.optimizers import Adam
from keras.regularizers import l2, l1
import tensorflow as tf
from sklearn.utils import shuffle


# physical_device = tf.config.list_logical_devices("GPU")
# tf.config.experimental.set_memory_growth(physical_device[0], True)


seed = 42
np.random.seed(seed)

df_train = pd.read_csv(r"U:\\PA AI\\data\\general\\training_data_v3.csv")
df_train = shuffle(df_train)

ds = tf.data.Dataset.from_tensor_slices((df_train[df_train.columns[2:]].astype("float32").values, df_train["sales"].astype("float32").values))
test_dataset = ds.take(20000) 
val_dataset = ds.take(10000)
train_dataset = ds.skip(30000)


class myDense(keras.layers.Layer):
    def __init__(self, units, input_dim):
        super(myDense, self).__init__()
        
        self.w = self.add_weight(
            shape=(input_dim, units),
            initializer="glorot_uniform",
            trainable=True,
            regularizer = myReg(0.001)
        )
        self.b = self.add_weight(
            shape=(units,), initializer="random_normal", trainable=True
        )

    def __call__(self, inputs):
        return tf.matmul(inputs, self.w) + self.b
    


class myRelu(keras.layers.Layer):
    def __init__(self):
        super(myRelu, self).__init__()

    def __call__(self, x):
        return tf.math.maximum(x, 0)
    
    
class myReg(keras.regularizers.Regularizer):
    def __init__(self, strength):
        super(myReg, self).__init__()
        self.strength = strength

    def __call__(self, x):
        return self.strength * tf.reduce_sum(tf.square(x))


class myModel(keras.Model):
    def __init__(self):
        super(myModel, self).__init__()
        self.dense1 = myDense(90, 72)
        self.dense2 = myDense(60, 90)
        self.dense3 = myDense(30, 60)
        self.dense4 = myDense(15, 30)
        self.dense5 = myDense(1, 15)
        self.relu = myRelu()

    def __call__(self, input_tensor, training = True):
        x = self.relu(self.dense1(input_tensor))
        x = self.relu(self.dense2(x))
        x = self.relu(self.dense3(x))
        x = self.relu(self.dense4(x))
        return keras.activations.linear(self.dense5(x))
    
model = myModel()

BATCH_SIZE = 32
AUTOTUNE = tf.data.experimental.AUTOTUNE

train_dataset = train_dataset.batch(BATCH_SIZE)
train_dataset = train_dataset.prefetch(AUTOTUNE)

test_dataset = test_dataset.batch(BATCH_SIZE)
test_dataset = test_dataset.prefetch(AUTOTUNE)

val_dataset = val_dataset.batch(BATCH_SIZE)
val_dataset = val_dataset.prefetch(AUTOTUNE)

epochs = 100
optimizer = tf.keras.optimizers.Adam(lr=0.001)
loss_fn  = keras.losses.MeanSquaredError()
acc_metric = keras.metrics.MeanAbsoluteError()
val_metric = keras.metrics.MeanAbsoluteError()

##Train loop
for epoch in range(epochs):
    print("Start of Traing epoch {}".format(epoch+1))
    for batch_idx, (x_batch, y_batch) in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            y_pred = model(x_batch, training = True)
            loss = loss_fn(y_batch, y_pred)

        gradients = tape.gradient(loss, model.trainable_weights)
        optimizer.apply_gradients(zip(gradients, model.trainable_weights))
        acc_metric.update_state(y_batch, y_pred)

    train_acc = acc_metric.result()
    print("Accuracy over epoch {}".format(train_acc))
    acc_metric.reset_states()

    for batch_idx, (x_batch, y_batch) in enumerate(val_dataset):
        y_pred = model(x_batch, training = False)
        val_loss = loss_fn(y_batch, y_pred)
        val_metric.update_state(y_batch, y_pred)

    print(f"Accuracy over validation set {val_metric.result()}")

    if val_loss > loss:
        print("Validation exceeded the train loss, consider lowering the number of epochs or use early stopping")

#Test loop
for batch_idx, (x_batch, y_batch) in enumerate(test_dataset):
    y_pred = model(x_batch, training = False)
    acc_metric.update_state(y_batch, y_pred)

train_acc = acc_metric.result()
print("Accuracy over Test Set: {}".format(train_acc))
acc_metric.reset_states()
