#!/usr/bin/env  python2.7
# -*- coding: utf-8 -*-

import numpy
import tensorflow as tf
import csv
import os.path

SCORE_SIZE = 3
HIDDEN_UNIT_SIZE = 16
TRAIN_DATA_SIZE = 15000

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('train_dir', '/tensorflow_dev/data',
                           """Directory where to write event logs """
                           """and checkpoint.""")
tf.app.flags.DEFINE_string('checkpoint_dir', '/tmp/data_train', '')

rows = []
with open('mansion.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        rows.append(row)

#numpy.random.shuffle(rows)

score = []
salary = []

for row in rows:
    score.append([numpy.float32(row[1]), numpy.float32(row[2]) * numpy.float32(row[4]), numpy.float32(row[3])])
    salary.append([numpy.float32(row[0])])

[salary_train, salary_test] = numpy.vsplit(salary, [TRAIN_DATA_SIZE])
[score_train, score_test] = numpy.vsplit(score, [TRAIN_DATA_SIZE])
[save_rows_train, save_rows_test] = numpy.vsplit(rows, [TRAIN_DATA_SIZE])

def inference(score_placeholder):
    with tf.name_scope('hidden1') as scope:
        hidden1_weight = tf.Variable(tf.truncated_normal([SCORE_SIZE, HIDDEN_UNIT_SIZE], stddev=0.1), name="hidden1_weight")
        hidden1_bias = tf.Variable(tf.constant(0.1, shape=[HIDDEN_UNIT_SIZE]), name="hidden1_bias")
        hidden1_output = tf.nn.relu(tf.matmul(score_placeholder, hidden1_weight) + hidden1_bias)
    with tf.name_scope('output') as scope:
        output_weight = tf.Variable(tf.truncated_normal([HIDDEN_UNIT_SIZE, 1], stddev=0.1), name="output_weight")
        output_bias = tf.Variable(tf.constant(0.1, shape=[1]), name="output_bias")
        output = tf.matmul(hidden1_output, output_weight) + output_bias
    return tf.nn.l2_normalize(output, 0)

def loss(output, salary_placeholder):
    with tf.name_scope('loss') as scope:
        loss = tf.nn.l2_loss(output - tf.nn.l2_normalize(salary_placeholder, 0))
        tf.scalar_summary(loss_label_placeholder, loss)
    return loss

with tf.Graph().as_default():
    salary_placeholder = tf.placeholder("float", [None, 1], name="salary_placeholder")
    score_placeholder = tf.placeholder("float", [None, SCORE_SIZE], name="score_placeholder")
    loss_label_placeholder = tf.placeholder("string", name="loss_label_placeholder")
    test_placeholder = tf.placeholder("float", [None, 1], name="test_placeholder")

    feed_dict_test={
        salary_placeholder: salary_test,
        score_placeholder: score_test,
        loss_label_placeholder: "loss_test"
    }

    output = inference(score_placeholder)
    loss = loss(output, salary_placeholder)

    best_loss = float("inf")

    near_val = 10000.0

    aaa = numpy.sqrt(sum(salary_test * salary_test))


    with tf.Session() as sess:
        saver = tf.train.Saver(tf.all_variables())
        saver.restore(sess, "/tmp/data_train/model.ckpt")

        loss_test = sess.run(loss, feed_dict=feed_dict_test)
        print(loss_test * aaa)
        best_match = sess.run(output, feed_dict=feed_dict_test)

    bbb = best_match * aaa
    file_name = 'result.csv'
    f = open(file_name, 'w')
    for i in range(len(bbb)):
        f.write("%f,%f,%d,%d,%f,%d,%d,%s\r\n" %
                (abs(salary_test[i][0] / bbb[i][0] - 1),
                bbb[i][0],
                int(save_rows_test[i][0]),
                int(save_rows_test[i][1]),
                float(save_rows_test[i][2]),
                int(save_rows_test[i][3]),
                int(save_rows_test[i][4]),
                save_rows_test[i][5]))
    f.close()
