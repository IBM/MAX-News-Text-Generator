import logging
import os
import re
from maxfw.model import MAXModelWrapper

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):
    """Model wrapper for Keras models"""

    MODEL_NAME = 'lm_1b'
    MODEL_LICENSE = "Apache v2"
    MODEL_META_DATA = {
        'id': '{}'.format(MODEL_NAME.lower()),
        'name': '{} TensorFlow Model'.format(MODEL_NAME),
        'description': 'Generative language model trained on the One Billion Words data set',
        'type': 'Generative Language Model',
        'license': '{}'.format(MODEL_LICENSE)
    }

    def __init__(self):
        pass

    def read_text(self, text_data):
        text = text_data.decode("utf-8")
        return text

    def predict(self, x):
        # this model does not like punctuation touching characters
        x = re.sub('([.,!?()])', r' \1 ', x)  # https://stackoverflow.com/a/3645946/

        os.system("python lm_1b/lm_1b_eval.py --mode sample \
                                     --prefix \"" + x + "\" \
                                     --pbtxt assets/data/graph-2016-09-10.pbtxt \
                                     --vocab_file assets/data/vocab-2016-09-10.txt  \
                                     --ckpt 'assets/data/ckpt-*' \
                                     --num_samples 1")

        try:
            txt_file = open("out.txt", "r")
        except OSError:
            print("Error generating a prediction, this is likely due to a lack of memory allocated to Docker")
            print("The minimum recommended resources for this model is 8 GB Memory and 4 CPUs")
        else:
            txt = txt_file.read()
            txt_file.close()
            return txt
