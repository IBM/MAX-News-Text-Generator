from flask_restplus import fields
from werkzeug.datastructures import FileStorage
from core.model import ModelWrapper
from maxfw.core import MAX_API, PredictAPI

input_parser = MAX_API.parser()
input_parser.add_argument('text', type=FileStorage, location='files', required=True, help='A text file')

predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'pred_txt': fields.String(required=True, description='Generated text based on input')
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        text_data = args['text'].read()
        text = self.model_wrapper.read_text(text_data)
        preds = self.model_wrapper.predict(text)

        result['pred_txt'] = preds
        result['status'] = 'ok'

        return result
