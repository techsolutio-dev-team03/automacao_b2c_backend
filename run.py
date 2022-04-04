#!/home/hulrich/PycharmProjects/automacao_b2c/venv/bin/python3.8
from connector import app

if __name__ == '__main__':
    
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)
