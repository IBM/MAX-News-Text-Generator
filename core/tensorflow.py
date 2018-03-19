import logging
import os

logger = logging.getLogger()


def read_text(text_data):
    text = text_data.decode("utf-8")
    return text


class ModelWrapper(object):
    """Model wrapper for Keras models"""
    def __init__(self):
        pass

    def predict(self, x):
        os.system("bazel-bin/lm_1b/lm_1b_eval --mode sample \
                                     --prefix \"" + x + "\" \
                                     --pbtxt data/graph-2016-09-10.pbtxt \
                                     --vocab_file data/vocab-2016-09-10.txt  \
                                     --ckpt 'data/ckpt-*' \
                                     --num_samples 1")

        txt_file = open("out.txt", "r")
        txt = txt_file.read()
        txt_file.close()
        return txt
