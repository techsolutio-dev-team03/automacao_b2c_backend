import requests

def update_test_progress(flask_username=None, progress=None, host='127.0.0.1', port=5000):
    flask_url = f'http://{host}:{port}/biz/update_session?username={flask_username}'
    data = {'progress': progress, 'username': flask_username}
    requests.post(url=flask_url, json=data)

