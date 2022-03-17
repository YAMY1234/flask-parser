import os
from flask import Flask
from basic import basic
# from flask_cors import CORS, cross_origin


app=Flask(__name__)
app = Flask(__name__, template_folder='templates')

from flask_wtf.csrf import CsrfProtect
CsrfProtect(app)

# 文件有关配置
UPLOAD_FOLDER = 'source_file'#文件下载路径
ALLOWED_EXTENSIONS = set(['json'])#文件允许上传格式
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#设置文件下载路径
app.register_blueprint(basic)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

if __name__=='__main__':
    app.run(
        debug=True,
        host = '127.0.0.1',
        port = 5000
    )