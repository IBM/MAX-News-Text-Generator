import logging
import os
import re

logger = logging.getLogger()


def read_text(text_data):
    text = text_data.decode("utf-8")
    return text


class ModelWrapper(object):
    """Model wrapper for Keras models"""
    def __init__(self):
        pass

    def predict(self, x):
        # this model does not like punctuation touching characters
        x = re.sub('([.,!?()])', r' \1 ', x)  # https://stackoverflow.com/a/3645946/

        os.system("python lm_1b/lm_1b_eval.py --mode sample \
                                     --prefix \"" + x + "\" \
                                     --pbtxt assets/data/graph-2016-09-10.pbtxt \
                                     --vocab_file assets/data/vocab-2016-09-10.txt  \
                                     --ckpt 'assets/data/ckpt-*' \
                                     --num_samples 1")

        txt_file = open("out.txt", "r")
        txt = txt_file.read()
        txt_file.close()
        return txt
