#从app模块中即从__init__.py中导入创建的app应用
from app import app
from . import db, Response, request
import json,sys

from sklearn import manifold,datasets
from .data.process import queryById, dataCal2, getPRecord, recordsKeys
from .fs.tsne import getResult, getPCA, fs, dimReduction

from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()


#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
@app.route('/')
@app.route('/index')
def index():
    return "Hello,World!"

# 用于展示原始数据
@app.route('/data')
def dataCal_init():
    data = dataCal2()
    data['data_norm'] = data['data_norm'].tolist()
    response = Response(json.dumps(data), mimetype='application/json')
    return response
    #return X_norm
@app.route('/process', methods=['POST'])
def process():
    req = request.json
    idx = req[u'idx']
    features = req[u'features']
    clusters = req[u'clusters']
    opt = {'randomState':50,'perplexity':30,'early_exaggeration':12.0, 'n_components':2}

    res = queryById(idx)
    records = []
    for item in res:
        records.extend(getPRecord(res[item], idx))
    tSNEInput = vec.fit_transform(records).toarray()
    names = vec.get_feature_names()
    ori_names = recordsKeys(records)
    rdData = dimReduction(tSNEInput, opt)
    features = fs(tSNEInput, features, clusters)
    ans = {
        'tsne': rdData,
        'ori_names': ori_names,
        'names': names,
        'features': features['idx'],
        'records': records
    }
    response = Response(json.dumps(ans), mimetype='application/json')
    return response

@app.route('/tsne', methods=['POST'])
def tsne():
    req = request.json
    idx = req[u'idx']
    opt = {'randomState': req[u'randomState'],'perplexity':req[u'perplexity'],'early_exaggeration':req[u'early_exaggeration'], 'n_components':req[u'n_components']}

    res = queryById(idx)
    records = []
    for item in res:
        records.extend(getPRecord(res[item], idx))
    tSNEInput = vec.fit_transform(records).toarray()
    names = vec.get_feature_names()
    rdData = dimReduction(tSNEInput, opt)
    ans = {
        'tsne': rdData
    }
    response = Response(json.dumps(ans), mimetype='application/json')
    return response

@app.route('/fs', methods=['POST'])
def featureSelection():
    req = request.json
    idx = req[u'idx']
    features = req[u'features']
    clusters = req[u'clusters']

    res = queryById(idx)
    records = []
    for item in res:
        records.extend(getPRecord(res[item], idx))
    tSNEInput = vec.fit_transform(records).toarray()
    names = vec.get_feature_names()
    ori_names = recordsKeys(records)
    features = fs(tSNEInput, features, clusters)
    ans = {
        'ori_names': ori_names,
        'names': names,
        'features': features['idx'],
        'records': records
    }
    response = Response(json.dumps(ans), mimetype='application/json')
    return response

@app.route("/getDRResult", methods=['POST'])
def getDRResult():
    req = request.json
    # rt = {'info': 'succeed'}
    result = getResult(indexes=req[u'indexes'],
                       dimensions=req[u'dimensions'],
                       isDataProjection=req[u'isDataProjection'],
                       randomState=req[u'tsneConfiguration'][u'randomState'],
                       perplexity=req[u'tsneConfiguration'][u'perplexity']
                       )
    rt = {
        'data': result
    }
    response = Response(json.dumps(rt), mimetype='application/json')
    return response

@app.route("/getPCAR", methods=["POST"])
def getPCAR():
    req = request.json
    # rt = {'info': 'succeed'}
    result = getPCA(indexes=req[u'indexes'],
                       dimensions=req[u'dimensions'],
                       num=req[u'num']
                       )
#    rt = {
#        'data': result
#    }
#    print(result)
    response = Response(json.dumps(result), mimetype='application/json')
    return response