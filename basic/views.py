from werkzeug.utils import secure_filename
from . import basic
import json
import os
from .main import *
from .maketree import *

from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, make_response

def allowed_file_json(filename):  # 通过将文件名分段的方式查询文件格式是否在允许上传格式范围之内
    return '.' in filename and filename.rsplit('.', 1)[1] in ['json']


tokens = get_tokens(0, '')
treedata = getS()
LR1 = getLR1()
stackTB = getstack()
SemanticData = getSemantic()
SemanticError = getSemanticError()
# print(stackTB)

# 这里是初始数据
# initdata="int main(){\n\tint a==1;\n\tint b=2;\n\tfloat c=3.28;\n\tif (a+b>c)\n\t{\n\t\treturn 1;\n\t}else{\n\t\treturn 0;\n\t}\n}"
# initdata = "int m;\nint n;\n int p;\nint main(){\n\tint a=1;\n\tint b=2;\n\tfloat c=3.28;\n\tif (a+b>c)\n\t{\n\t\treturn 1;\n\t}else{\n\t\treturn 0;\n\t}\n}"
initdata = "int a;\nint b;\nint program(int a, int b, int c)\n{\n	int i;\n	int j;\n	i = 0;\n	if (a > (b + c))\n	{\n		j = a + (b * c + 1);\n	}\n	else\n	{\n		j = a;\n	}\n	while (i <= 100)\n	{\n		i = j * 2;\n	}\n	return i;\n}\n\nint demo(int a)\n{\n	a = a + 2;\n	return a * 2;\n}\nint main()\n{\n	int a;\n	int b;\n	int c;\n	a = 3;\n	b = 4;\n	c = 2;\n	a = program(a, b, demo(c));\n	return;\n}\n"

@basic.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':  # 当以post方式提交数据时
        inputdata = request.form.get('inputcode')
        if inputdata != '':
            token_disposed, res_token, res_ana, error_token = get_tokens(
                1, inputdata)
            treedata_disposed = getS()
            LR1_disposed = getLR1()
            stackTB_disposed = getstack()
            # write_my_intermediate_code()
            SemanticData_disposed = getSemantic()
            SemanticError_disposed = getSemanticError()
            print(SemanticError_disposed)
            # printSymbolTable()
            return render_template('index.html',
                                   tokens=token_disposed,
                                   treedata=treedata_disposed,
                                   LR1=LR1_disposed,
                                   stackTB=stackTB_disposed,
                                   SemanticData=SemanticData_disposed,
                                   SemanticError=SemanticError_disposed,
                                   mode=1,
                                   initdata='',
                                   yourcode=inputdata,
                                   res_token=res_token,
                                   res_ana=res_ana,
                                   error_token=error_token)
        else:
            pass
    return render_template('index.html',
                           tokens=tokens,
                           treedata=treedata,
                           LR1=LR1, stackTB=stackTB,
                           SemanticData=SemanticData,
                           SemanticError=SemanticError,
                           mode=0,
                           initdata=initdata,
                           yourcode="\"you haven't enter your code yet!\"")


@basic.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # 当以post方式提交数据时
        file = request.files['file']  # 将上传的文件赋予file
        if file and allowed_file_json(file.filename):  # 当确认有上传文件并且格式合法
            basepath = os.getcwd()
            upload_path = os.path.join(basepath, 'source_file', 'grammer.json')
            file.save(upload_path)
            message = 0
            # flash('上传成功')
        else:
            message = 1
            flash('上传失败')
    return render_template('index.html',
                           tokens=tokens,
                           treedata=treedata,
                           LR1=LR1,
                           stackTB=stackTB,
                           SemanticData=SemanticData,
                           SemanticError=SemanticError,
                           mode=0,
                           initdata=initdata,
                           msg=message,
                           yourcode="\"you haven't enter your code yet!\"")


@basic.route('/index')
def index():
    return render_template('index.html')
