# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import csv
import numpy


trX1 = []
trX2 = []
trX3 = []
trY = []

with open('mansion.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        trX1.append(np.float32(row[1]))
        trX2.append(np.float32(row[2]))
        trX3.append(np.float32(row[3]))
        trY.append(np.float32(row[0]))

def lin_model(X1, w1, X2, w2, X3, w3, b):
    return X1 * w1 + X2 * w2 + X3 * w3 + b

w1 = tf.Variable([0.])
w2 = tf.Variable([0.])
w3 = tf.Variable([0.])
b = tf.Variable([0.])

data_size = len(trY)

x1 = tf.placeholder(tf.float32, shape=(data_size))
x2 = tf.placeholder(tf.float32, shape=(data_size))
x3 = tf.placeholder(tf.float32, shape=(data_size))
y = tf.placeholder(tf.float32, shape=(data_size))
y_hypo = lin_model(x1, w1, x2, w2, x3, w3, b)

cost = tf.reduce_mean(tf.square(y_hypo - y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

# Initializing
init = tf.initialize_all_variables()

# Train
with tf.Session() as sess:
    sess.run(init)
    trX1 = sess.run(tf.nn.l2_normalize(trX1, 0))
    trX2 = sess.run(tf.nn.l2_normalize(trX2, 0))
    trX3 = sess.run(tf.nn.l2_normalize(trX3, 0))
    trY = sess.run(tf.nn.l2_normalize(trY, 0))

    for i in range(100001):
        sess.run(train_step, feed_dict={x1: trX1, x2: trX2, x3: trX3, y: trY})
        if i % 100 == 0:
            print "%5d:(w1,w2,w3,b)=(%10.4f, %10.4f, %10.4f, %10.4f)" % (i, sess.run(w1), sess.run(w2), sess.run(w3), sess.run(b))
