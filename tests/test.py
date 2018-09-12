import pytest
import requests


def test_response():
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
