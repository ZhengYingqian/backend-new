# -*- coding:utf-8 -*-
#从app模块中导入app应用
from app import app
from waitress import serve

app.debug = True
#防止被引用后执行，只有在当前模块中才可以使用
# if __name__=='__main__':
#     app.run(
#         host='202.117.54.60',
#         port= 5000,
#         debug=True)
serve(app, listen='202.117.54.60:5000')