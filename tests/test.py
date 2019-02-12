import pytest
import requests
import os


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'Model Asset Exchange Microservice'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'lm_1b'
    assert metadata['name'] == 'lm_1b TensorFlow Model'
    assert metadata['description'] == 'Generative language model trained on the One Billion Words data set'
    assert metadata['license'] == 'Apache v2'


@pytest.mark.skipif("TRAVIS" in os.environ, reason="test runs out of memory on Travis-CI")
def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'data/sample1.txt'

    with open(file_path, 'rb') as file:
        file_form = {'text': (file_path, file, 'text/plain')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200

    response = r.json()

    assert response['status'] == 'ok'
    assert len(response['pred_txt']) > 14  # output should contain more chars than input

    print("output: " + response['pred_txt'])


if __name__ == '__main__':
    pytest.main([__file__])
