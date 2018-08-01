# Application settings

# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'lm_1b'

MODEL_LICENSE = "Apache v2"

MODEL_META_DATA = {
    'id': '{}'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': 'Generative language model trained on the One Billion Words data set',
    'type': 'Generative Language Model',
    'license': '{}'.format(MODEL_LICENSE)
}
