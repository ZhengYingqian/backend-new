# -*- coding:utf-8 -*-
from flask import Flask, request, Response
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
# 连接数据库
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/oncology'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/project'
# 请求结束后自动提交数据库变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了
db.init_app(app)

from app import routes