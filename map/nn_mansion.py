#!/usr/bin/env  python2.7
# -*- coding: utf-8 -*-

import numpy
import tensorflow as tf
import os.path
import logging
LOG = logging.getLogger(__file__)
LOG.info('START')

IN_DATA_COL_NUM = 4
HIDDEN_UNIT_SIZE = 18
HIDDEN2_UNIT_SIZE = 12

FLAGS = tf.app.flags.FLAGS

lines = []

STDDEV=0.3
BIAS=0.1
LEARNING_RATE=0.005
HIDDEN_UNIT_SIZE=32
HIDDEN2_UNIT_SIZE=16

LOG.info('STDDEV %s' % (STDDEV))
LOG.info('BIAS %s' % (BIAS))
LOG.info('LEARNING_RATE %s' % (LEARNING_RATE))
LOG.info('HIDDEN_UNIT_SIZE %s' % (HIDDEN_UNIT_SIZE))
LOG.info('HIDDEN2_UNIT_SIZE %s' % (HIDDEN2_UNIT_SIZE))

training_dir = 'data' + str(HIDDEN_UNIT_SIZE) + '_' + str(HIDDEN2_UNIT_SIZE)
tf.app.flags.DEFINE_string('train_dir', './' + training_dir,
                           """Directory where to write event logs """
                           """and checkpoint.""")

def inference(in_data_placeholder):
    with tf.name_scope('hidden1') as scope:
        hidden1_weight = tf.Variable(tf.truncated_normal([IN_DATA_COL_NUM, HIDDEN_UNIT_SIZE], stddev=STDDEV), name="hidden1_weight")
        hidden1_bias = tf.Variable(tf.constant(BIAS, shape=[HIDDEN_UNIT_SIZE]), name="hidden1_bias")
        hidden1_output = tf.nn.relu(tf.matmul(in_data_placeholder, hidden1_weight) + hidden1_bias)
    with tf.name_scope('hidden2') as scope:
        hidden2_weight = tf.Variable(tf.truncated_normal([HIDDEN_UNIT_SIZE, HIDDEN2_UNIT_SIZE], stddev=STDDEV), name="hidden2_weight")
        hidden2_bias = tf.Variable(tf.constant(BIAS, shape=[HIDDEN2_UNIT_SIZE]), name="hidden2_bias")
        hidden2_output = tf.nn.relu(tf.matmul(hidden1_output, hidden2_weight) + hidden2_bias)
    with tf.name_scope('output') as scope:
        output_weight = tf.Variable(tf.truncated_normal([HIDDEN2_UNIT_SIZE, 1], stddev=STDDEV), name="output_weight")
        output_bias = tf.Variable(tf.constant(BIAS, shape=[1]), name="output_bias")
        output = tf.matmul(hidden2_output, output_weight) + output_bias
    return output


class NnMansion(object):
    def __init__(self):
        pass

    @staticmethod
    def predict_by_array(in_params):
        [in_param_train, in_param_test] = numpy.vsplit(in_params, [0])

        with tf.Graph().as_default():
            reverse_price_var = tf.Variable(0.0, name="reverse_price")
            reverse_predval_var = tf.Variable(0.0, name="reverse_predval")
            in_data_placeholder = tf.placeholder("float", [None, IN_DATA_COL_NUM], name="in_data_placeholder")

            feed_dict_test={
                in_data_placeholder: in_param_test,
            }

            output = inference(in_data_placeholder)

            # Create a saver.
            saver = tf.train.Saver(tf.all_variables())

            with tf.Session() as sess:
                LOG.info("load checkpoint")
                checkpoint_path = os.path.join(FLAGS.train_dir, 'best_model_best.ckpt')
                saver.restore(sess, checkpoint_path)

                LOG.info('-----')
                LOG.info(sess.run(reverse_price_var))
                LOG.info(sess.run(reverse_predval_var))
                LOG.info('-----')

                best_match = sess.run(output, feed_dict=feed_dict_test)
                normalized = best_match / sess.run(reverse_predval_var)
#                LOG.info("best " + str(best_match))
#                LOG.info("price " +  str(normalized))
#                LOG.info("price " +  str(normalized * sess.run(reverse_price_var)))
                return (normalized.transpose()[0] * sess.run(reverse_price_var) * numpy.array(in_params)[:,1])

    @staticmethod
    def predict(year, occupied, walk, rosen):
        in_params = []
        in_params.append([
            numpy.float32(year),
            numpy.float32(occupied),
            numpy.float32(walk),
            numpy.float32(rosen)])
        return NnMansion.predict_by_array(in_params)
