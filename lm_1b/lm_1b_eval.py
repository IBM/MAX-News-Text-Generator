# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Eval pre-trained 1 billion word language model.
"""

import sys
import numpy as np
from six.moves import xrange
import tensorflow as tf
from google.protobuf import text_format
import lm_1b.data_utils as data_utils

_VOCAB_FILE = "assets/data/vocab-2016-09-10.txt"
_PBTXT = "assets/data/graph-2016-09-10.pbtxt"
_CKPT = 'assets/data/ckpt-*'
_NUM_SAMPLES = 1
_MAX_SAMPLE_WORDS = 100

# For saving demo resources, use batch size 1 and step 1.
BATCH_SIZE = 1
NUM_TIMESTEPS = 1
MAX_WORD_LEN = 50


def _LoadModel(gd_file, ckpt_file):
    """Load the model from GraphDef and Checkpoint.

    Args:
      gd_file: GraphDef proto text file.
      ckpt_file: TensorFlow Checkpoint file.

    Returns:
      TensorFlow session and tensors dict.
    """
    with tf.Graph().as_default():
        sys.stderr.write('Recovering graph.\n')
        with tf.gfile.FastGFile(gd_file, 'r') as f:
            s = f.read()  # .decode()
            gd = tf.GraphDef()
            text_format.Merge(s, gd)

        tf.logging.info('Recovering Graph %s', gd_file)
        t = {}
        [t['states_init'], t['lstm/lstm_0/control_dependency'],
         t['lstm/lstm_1/control_dependency'], t['softmax_out'], t['class_ids_out'],
         t['class_weights_out'], t['log_perplexity_out'], t['inputs_in'],
         t['targets_in'], t['target_weights_in'], t['char_inputs_in'],
         t['all_embs'], t['softmax_weights'], t['global_step']
         ] = tf.import_graph_def(gd, {}, ['states_init',
                                          'lstm/lstm_0/control_dependency:0',
                                          'lstm/lstm_1/control_dependency:0',
                                          'softmax_out:0',
                                          'class_ids_out:0',
                                          'class_weights_out:0',
                                          'log_perplexity_out:0',
                                          'inputs_in:0',
                                          'targets_in:0',
                                          'target_weights_in:0',
                                          'char_inputs_in:0',
                                          'all_embs_out:0',
                                          'Reshape_3:0',
                                          'global_step:0'], name='')

        sys.stderr.write('Recovering checkpoint %s\n' % ckpt_file)
        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        sess.run('save/restore_all', {'save/Const:0': ckpt_file})
        sess.run(t['states_init'])

    return sess, t


def _SampleSoftmax(softmax):
    return min(np.sum(np.cumsum(softmax) < np.random.rand()), len(softmax) - 1)


def _SampleModel(prefix_words, vocab):
    """Predict next words using the given prefix words.

    Args:
      prefix_words: Prefix words.
      vocab: Vocabulary. Contains max word chard id length and converts between
          words and ids.
    """
    targets = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
    weights = np.ones([BATCH_SIZE, NUM_TIMESTEPS], np.float32)

    sess, t = _LoadModel(_PBTXT, _CKPT)

    if prefix_words.find('<S>') != 0:
        prefix_words = '<S> ' + prefix_words

    prefix = [vocab.word_to_id(w) for w in prefix_words.split()]
    prefix_char_ids = [vocab.word_to_char_ids(w) for w in prefix_words.split()]
    for _ in xrange(_NUM_SAMPLES):
        inputs = np.zeros([BATCH_SIZE, NUM_TIMESTEPS], np.int32)
        char_ids_inputs = np.zeros(
            [BATCH_SIZE, NUM_TIMESTEPS, vocab.max_word_length], np.int32)
        samples = prefix[:]
        char_ids_samples = prefix_char_ids[:]
        sent = ''
        while True:
            inputs[0, 0] = samples[0]
            char_ids_inputs[0, 0, :] = char_ids_samples[0]
            samples = samples[1:]
            char_ids_samples = char_ids_samples[1:]

            softmax = sess.run(t['softmax_out'],
                               feed_dict={t['char_inputs_in']: char_ids_inputs,
                                          t['inputs_in']: inputs,
                                          t['targets_in']: targets,
                                          t['target_weights_in']: weights})

            sample = _SampleSoftmax(softmax[0])
            sample_char_ids = vocab.word_to_char_ids(vocab.id_to_word(sample))

            if not samples:
                samples = [sample]
                char_ids_samples = [sample_char_ids]
            sent += vocab.id_to_word(samples[0]) + ' '
            sys.stderr.write('%s\n' % sent)

            if vocab.id_to_word(samples[0]) == '</S>' or len(sent) > _MAX_SAMPLE_WORDS:
                return sent


def generate(prefix):
    vocab = data_utils.CharsVocabulary(_VOCAB_FILE, MAX_WORD_LEN)

    return _SampleModel(prefix, vocab)


if __name__ == '__main__':
    tf.app.run()
