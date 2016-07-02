#!/usr/bin/env  python2.7
# -*- coding: utf-8 -*-

import sys
import numpy
import tensorflow as tf
import csv
import os.path

IN_DATA_COL_NUM = 5
HIDDEN_UNIT_SIZE = 18
HIDDEN2_UNIT_SIZE = 12
TRAIN_DATA_SIZE = 15000

FLAGS = tf.app.flags.FLAGS

lines = []
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    IN_DATA_COL_NUM = len(reader.next()) - 2
    IN_DATA_COL_NUM -= 1
    for row in reader:
        lines.append(row)
print('IN_DATA_COL_NUM = ' + str(IN_DATA_COL_NUM))
TRAIN_DATA_SIZE = int(len(lines) / 2)
print('TRAIN_DATA_SIZE = %d' % TRAIN_DATA_SIZE)

STDDEV=float(sys.argv[2]) if len(sys.argv) > 1 else 0.05
BIAS=float(sys.argv[3]) if len(sys.argv) > 2 else 0.1
LEARNING_RATE=float(sys.argv[4]) if len(sys.argv) > 3 else 0.001
HIDDEN_UNIT_SIZE=int(sys.argv[5]) if len(sys.argv) > 4 else 16
HIDDEN2_UNIT_SIZE=int(sys.argv[6]) if len(sys.argv) > 5 else 8
TRAINING_COUNT=int(sys.argv[7]) if len(sys.argv) > 6 else 30001

print('STDDEV %s' % (STDDEV))
print('BIAS %s' % (BIAS))
print('LEARNING_RATE %s' % (LEARNING_RATE))
print('HIDDEN_UNIT_SIZE %s' % (HIDDEN_UNIT_SIZE))
print('HIDDEN2_UNIT_SIZE %s' % (HIDDEN2_UNIT_SIZE))
print('TRAINING_COUNT %s' % (TRAINING_COUNT))

training_dir = 'data' + str(HIDDEN_UNIT_SIZE) + '_' + str(HIDDEN2_UNIT_SIZE)
tf.app.flags.DEFINE_string('train_dir', '/tensorflow_dev/' + training_dir,
                           """Directory where to write event logs """
                           """and checkpoint.""")

numpy.random.shuffle(lines)

in_params = []
mansion_prices = []
normalized_prices = []

index_of_price = 0
index_of_year = 1
index_of_occupied = 2
index_of_walk = 3
index_of_posted = 4
index_of_rosen = 5
index_of_url = 6

for row in lines:
    in_params.append([
        numpy.float32(row[index_of_year]),
        numpy.float32(row[index_of_occupied]),
        numpy.float32(row[index_of_walk]),
        numpy.float32(row[index_of_rosen])])
    mansion_prices.append([numpy.float32(row[index_of_price])])
np_mansion_prices = numpy.array(mansion_prices)

[price_train, price_test] = numpy.vsplit(np_mansion_prices, [TRAIN_DATA_SIZE])
[in_param_train, in_param_test] = numpy.vsplit(in_params, [TRAIN_DATA_SIZE])
[save_rows_train, save_rows_test] = numpy.vsplit(lines, [TRAIN_DATA_SIZE])


def inference(in_data_placeholder):
    with tf.name_scope('hidden1') as scope:
        hidden1_weight = tf.Variable(tf.truncated_normal([IN_DATA_COL_NUM, HIDDEN_UNIT_SIZE], stddev=STDDEV), name="hidden1_weight")
        hidden1_bias = tf.Variable(tf.constant(BIAS, shape=[HIDDEN_UNIT_SIZE]), name="hidden1_bias")
        hidden1_output = tf.nn.relu(tf.matmul(in_data_placeholder, hidden1_weight) + hidden1_bias)
    with tf.name_scope('hidden2') as scope:
        hidden2_weight = tf.Variable(tf.truncated_normal([HIDDEN_UNIT_SIZE, HIDDEN2_UNIT_SIZE], stddev=STDDEV), name="hidden2_weight")
        hidden2_bias = tf.Variable(tf.constant(BIAS, shape=[HIDDEN2_UNIT_SIZE]), name="hidden2_bias")
        hidden2_output = tf.nn.relu(tf.matmul(hidden1_output, hidden2_weight) + hidden2_bias)
    with tf.name_scope('dropout') as scope:
        h_drop = tf.nn.dropout(hidden2_output, keep_prob)
    with tf.name_scope('output') as scope:
        output_weight = tf.Variable(tf.truncated_normal([HIDDEN2_UNIT_SIZE, 1], stddev=STDDEV), name="output_weight")
        output_bias = tf.Variable(tf.constant(BIAS, shape=[1]), name="output_bias")
        output = tf.matmul(h_drop, output_weight) + output_bias
    return output


def loss(output, price_placeholder):
    with tf.name_scope('loss') as scope:
        loss = tf.nn.l2_loss(tf.nn.l2_normalize(output, 0) - tf.nn.l2_normalize(price_placeholder, 0))
        tf.scalar_summary(loss_label_placeholder, loss)
    return loss


def training(loss):
    with tf.name_scope('training') as scope:
        train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(loss)
    return train_step

with tf.Graph().as_default():
    price_placeholder = tf.placeholder("float", [None, 1], name="price_placeholder")
    in_data_placeholder = tf.placeholder("float", [None, IN_DATA_COL_NUM], name="in_data_placeholder")
    loss_label_placeholder = tf.placeholder("string", name="loss_label_placeholder")
    test_placeholder = tf.placeholder("float", [None, 1], name="test_placeholder")
    keep_prob = tf.placeholder("float", name="keep_prob")
    reverse_price_var = tf.Variable(0.0, name="reverse_price")
    reverse_predval_var = tf.Variable(0.0, name="reverse_predval")


    feed_dict_train={
        price_placeholder: price_train,
        in_data_placeholder: in_param_train,
        loss_label_placeholder: "loss_train",
        keep_prob: 0.95,
    }

    feed_dict_test={
        price_placeholder: price_test,
        in_data_placeholder: in_param_test,
        loss_label_placeholder: "loss_test",
        keep_prob: 1.0,
    }

    output = inference(in_data_placeholder)
    loss = loss(output, price_placeholder)
    training_op = training(loss)

    # Create a saver.
    saver = tf.train.Saver(tf.all_variables())
    summary_op = tf.merge_all_summaries()

    best_loss = float("inf")

    with tf.Session() as sess:
        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph)

        if tf.train.get_checkpoint_state(FLAGS.train_dir):
            print("load checkpoint")
            ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
            last_model = ckpt.model_checkpoint_path
            saver.restore(sess, last_model)
        else:
            print("*** initial data ***")
            init = tf.initialize_all_variables()
            sess.run(init)

        predict_mansion_price = []
        for step in range(TRAINING_COUNT):
            sess.run(training_op, feed_dict=feed_dict_train)
            loss_test = sess.run(loss, feed_dict=feed_dict_test)
            if loss_test < best_loss:
                best_loss = loss_test
                predict_values = sess.run(output, feed_dict=feed_dict_test)
                reverse_price = numpy.sqrt(sum(price_test * price_test))
                reverse_predict_values = numpy.sqrt(sum(predict_values * predict_values))
                sess.run(tf.assign(reverse_price_var, float(reverse_price)))
                sess.run(tf.assign(reverse_predval_var, float(reverse_predict_values)))
                checkpoint_path = os.path.join(FLAGS.train_dir, 'best_model_best.ckpt')
                saver.save(sess, checkpoint_path)
                predict_mansion_price = predict_values / reverse_predict_values * reverse_price


            if step % 1000 == 0:
                print('best_loss %f' % (best_loss))
                summary_str = sess.run(summary_op, feed_dict=feed_dict_test)
                summary_writer.add_summary(summary_str, step)
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path)

            if step % 10000 == 0:
            	best_loss = float("inf")
            
                file_name = ('result%d.csv' % step)
                print('output ' + file_name)
                f = open(file_name, 'w')
                for i in range(len(predict_mansion_price)):
                    behind_price = abs(predict_mansion_price[i] * float(save_rows_test[i][index_of_occupied])) - float(save_rows_test[i][index_of_price])  * float(save_rows_test[i][index_of_occupied])
                    error_rate = float(behind_price) / (float(save_rows_test[i][index_of_price]) * float(save_rows_test[i][index_of_occupied]))
                    f.write("%f,%f,%f,%d,%f,%d,%d,%d,%s\r\n" %
                        (float(error_rate),
                        predict_mansion_price[i],
                        float(save_rows_test[i][index_of_price]),
                        int(save_rows_test[i][index_of_year]),
                        float(save_rows_test[i][index_of_occupied]),
                        int(save_rows_test[i][index_of_walk]),
                        int(save_rows_test[i][index_of_posted]),
                        int(save_rows_test[i][index_of_rosen]),
                        save_rows_test[i][index_of_url]))
                f.close()
