import numpy as np
import re
import time
from ..database import SECOND_FEE, SECOND_HOME, SECOND_LIS,HOME, FEE
from .data import home_info2, lis, shortLis
from .bi import searchKey
from .transKeys import dropKeys, selectKeys1, selectKeys2

# 根据id数组查询病案号
def queryById(ids):
    bahs = searchKey(ids, 'part1_pid', 'part1_bah')
    pats = {}
    for key in bahs:
        home = HOME.query.filter(HOME.part1_bah == key and HOME.part1_HIS == 1).all()
        home = HOME.query.filter(HOME.part1_bah == key and HOME.part1_HIS == 0).all()
        lisdata = SECOND_LIS.query.filter(SECOND_LIS.part3_OUTPATIENT_ID == key).all()
        if key in pats:
            pats[key]['home'].append(home)
            pats[key]['lisdata'].append(lisdata)
        else:
            pats[key] = {
                'home': home,
                'lisdata': lisdata
                }
    return pats;

# 将每个病人的home、fee、lis连接为若干条数据
def getPRecord(data, ids):
    res = []
    lisdata = data['lisdata']
    home = data['home']
    selectKeys = []
    selectKeys = concatKeys(selectKeys1, selectKeys2)
    #get rusj-cysj
    for item in home:
        temp = item.to_dict()
        # print(getattr(item, 'part1_rysj'), getattr(item, 'part1_cysj'))
        if '/' in getattr(item, 'part1_rysj') and '/' in getattr(item, 'part1_cysj'):
            timerange = [time.strptime(getattr(item, 'part1_rysj').split(' ')[0], '%Y/%m/%d'), time.strptime(getattr(item,'part1_cysj').split(' ')[0], '%Y/%m/%d')]
            for lisItem in lisdata:
                # TODO：对于lis检查项待处理 getattr(lisItem, 'part3_CHINESE_NAME')+ '_'+ getattr(lisItem, 'part3_TEST_ORDER_NAME')
                t1 = getattr(lisItem, 'part3_INSPECTION_DATE')
                t =time.mktime(time.strptime(t1, '%Y%m%d'))
                name = getattr(lisItem, 'part3_TEST_ORDER_NAME') 
                # val = getattr(lisItem, 'part3_QUANTITATIVE_RESULT')
                if t>time.mktime(timerange[0]) and t<time.mktime(timerange[1]) and getattr(lisItem, 'part3_QUANTITATIVE_RESULT') != None and '---' not in getattr(lisItem, 'part3_QUANTITATIVE_RESULT') :
                    temp[getattr(lisItem, 'part3_CHINESE_NAME')] = getattr(lisItem, 'part3_QUANTITATIVE_RESULT')
                    # if getattr(lisItem, 'part3_TEST_ORDER_NAME'):
                    #     temp[getattr(lisItem, 'part3_CHINESE_NAME')+'_'+getattr(lisItem, 'part3_TEST_ORDER_NAME')] = getattr(lisItem, 'part3_QUANTITATIVE_RESULT')
                else:
                    pass
                
            if temp['part1_pid'] in ids:
                # tt = dropKeyfn(temp, dropKeys)
                # tt = selectxcgKeyfn(temp, selectKeys)
                tt = appendReocrds(temp, selectKeys)
                # if len(tt) == len(selectKeys):
                res.append(tt)
    return res

# 获取共同的key
def recordsKeys(data):
    collectKeys=[]
    dics = {}
    for item in data:
        for key in item.keys():
            if key in collectKeys:
                dics[key] = dics[key]+1
            else:
                collectKeys.append(key)
                dics[key] = 1
    return dics
                
# 删去无关维度
def dropKeyfn(dic, keys):
    newDic = {}
    for key in dic:
        if key in keys:
            pass
        else:
            if is_number(dic[key]):
                newDic[key] = float(dic[key])
            else:
                newDic[key] = dic[key]
    return newDic
# 选择观察维度
def selectKeyfn(dic, keys):
    newDic = {}
    for key in dic:
        if key in keys:
            if is_number(dic[key]):
                newDic[key] = float(dic[key])
            else:
                newDic[key] = dic[key]
        else:
            pass
    return newDic
# 为空值补零
def appendReocrds(dic, keys):
    newDic = {}
    for key in keys:
        if key in dic:
            if is_number(dic[key]):
                newDic[key] = float(dic[key])
            else:
                newDic[key] = dic[key]
        else:
            newDic[key] = 0
    return newDic

def selectxcgKeyfn(dic, keys):
    newDic = {}
    for key in keys:
        if key in dic:
            if is_number(dic[key]):
                newDic[key] = float(dic[key])
            else:
                newDic[key] = dic[key]
    return newDic

def concatKeys(keys1, keys2):
    newKeys = keys2
    for ele in keys1:
        if ele not in keys2:
            newKeys.append(ele)
    return newKeys

# 获取全部的维度
def collectAllKeysfn(dic, keys):
    newKeys = []
    for key in dic:
        if key in keys:
            pass
        else:
            newKeys.append(key)
    return newKeys
# 提取共有维度guan
def commonKeysfn(dic, keys):
    newKeys = []
    for key in dic:
        if key in keys:
            newKeys.append(key)
        else:
            pass
    return newKeys
# 判断是否为数字
def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True

# 20190109：调整后的维度计算方法
def dataCal2():
    home = SECOND_HOME.query.filter(SECOND_HOME.part1_HIS == 1 ).all()
    data = []
    num = 0

    for rec in home:
        tmp = []
        for record in home_info2:
            if record == 'part1_xb' and getattr(rec, record) == 1:
                tmp.append(1)
                tmp.append(0)
            elif record == 'part1_xb' and getattr(rec, record) == 2:
                tmp.append(0)
                tmp.append(1)
            elif record == 'part1_cyzd1':
                tmp2 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
                if getattr(rec,record) == u'乳腺恶性肿瘤':
                    tmp = tmp + tmp2[0]
                elif getattr(rec,record) == u'乳腺腺病':
                    tmp = tmp + tmp2[1]
                elif getattr(rec,record) == u'浆细胞性乳腺炎':
                    tmp = tmp + tmp2[2]
                else:
                    tmp = tmp + tmp2[3]
            elif record == 'part1_mzfs':
                tmp2 = [[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]
                if getattr(rec,record) == '0102':
                    tmp = tmp + tmp2[0]
                elif getattr(rec,record) == '02':
                    tmp = tmp + tmp2[1]
                elif getattr(rec,record) == '0302':
                    tmp = tmp + tmp2[2]
                elif getattr(rec,record) == '0502':
                    tmp = tmp + tmp2[3]
                elif getattr(rec,record) == '0503':
                    tmp = tmp + tmp2[4]
                else :
                    tmp = tmp + tmp2[5]
            elif record == 'part1_ssmc':
                tmp2 = [[1, 0, 0,0], [0, 1, 0,0], [0, 0, 1,0],[0,0,0,1]]
                if getattr(rec, record) == u'乳房病损切除术':
                    tmp = tmp + tmp2[0]
                elif getattr(rec, record) == u'单侧乳房改良根治术':
                    tmp = tmp + tmp2[1]
                elif getattr(rec, record) == u'乳腺腺叶切除术':
                    tmp = tmp + tmp2[2]
                else:
                    tmp = tmp + tmp2[3]
            else:
                # print(getattr(rec,record))
                tmp.append(getattr(rec, record))
        num = len(tmp)
        data.append(tmp)

    carsData = np.array(data, dtype='float')
    X = np.reshape(carsData, (len(data), num))
    np.seterr(divide='ignore', invalid='ignore')
    # print(X)
    x_min, x_max = X.min(0), X.max(0)
    # x_min = x_min + sys.float_info.min
    # print(x_min)
    # print(x_max)
    X_norm = (X - x_min) / ((x_max - x_min) + 1e-40)

    # rt = {
    #   'data': data
    # }
    # response = Response(json.dumps(rt), mimetype='application/json')
    # return response

    #return X_norm
    result = {
        'length':len(data),
        'dim':num,
        'dimensions':[
             'part1_zycs',
             'part1_ylfkfs',
             'part1_nl',
             'part1_xb_m',
             'part1_xb_f',
             'part1_sjzyts',
             'part1_cyzd1_乳腺恶性肿瘤',
             'part1_cyzd1_乳腺腺病',
             'part1_cyzd1_浆细胞性乳腺炎',
             'part1_cyzd1_others',
             'part1_mzfs_0102',
             'part1_mzfs_02',
             'part1_mzfs_0302',
             'part1_mzfs_0502',
             'part1_mzfs_0503',
             'part1_mzfs_others',
             'part1_ssmc_乳房病损切除术',
             'part1_ssmc_单侧乳房改良根治术',
             'part1_ssmc_乳腺腺叶切除术',
             'part1_ssmc_others'
        ],
        'data_init':data,
        'data_norm':X_norm,
    }
    return result