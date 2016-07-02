# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import csv


trX = np.random.rand(101).astype(np.float32)
trY = 2 * trX + 3

def lin_model(X, w, b):
    return X * w + b

w = tf.Variable([0.])
b = tf.Variable([0.])

data_size = len(trY)

x = tf.placeholder(tf.float32, shape=(data_size))
y = tf.placeholder(tf.float32, shape=(data_size))
y_hypo = lin_model(x, w, b)

cost = tf.reduce_mean(tf.square(y_hypo - y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

# Initializing
init = tf.initialize_all_variables()

# Train
with tf.Session() as sess:
    sess.run(init)

    for i in range(100001):
        sess.run(train_step, feed_dict={x: trX, y: trY})
        if i % 100 == 0:
            print "%5d:(w,b)=(%10.4f, %10.4f)" % (i, sess.run(w), sess.run(b))
