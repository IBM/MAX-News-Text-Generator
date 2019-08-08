#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
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
#

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

        if preds is None:
            result['status'] = 'error'
        else:
            result['status'] = 'ok'

        result['pred_txt'] = preds

        return result
