from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from config import MODEL_META_DATA
from core.tensorflow import ModelWrapper, read_text

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


pred_txt = api.model('LabelPrediction', {
    'pred_txt': fields.String(required=True, description='List containing the generated text')
})


predict_response = api.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'pred_txt': fields.List(fields.Nested(pred_txt), description='Generated text based on input')
})

# set up parser for image input data
text_parser = api.parser()
text_parser.add_argument('text', type=FileStorage, location='files', required=True, help='A text file')


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(text_parser)
    @api.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = text_parser.parse_args()
        text_data = args['text'].read()
        text = read_text(text_data)
        preds = self.model_wrapper.predict(text)

        label_preds = [{'pred_txt': preds}]
        result['pred_txt'] = label_preds
        result['status'] = 'ok'

        return result
