# -*- coding: utf-8 -*-
######
##参考
##https://github.com/aliyun/aliyun-openapi-python-sdk/blob/master/aliyun-python-sdk-core/aliyunsdkcore/auth/composer/rpc_signature_composer.py?spm=5176.doc44434.2.2.lULUcI&file=rpc_signature_composer.py
##安装aliyun-python-sdk
##https://help.aliyun.com/document_detail/52613.html?spm=5176.doc55397.2.8.qkNXG2
######
__author__ = 'Jeiry'
from aliyunsdkcore.auth.algorithm import sha_hmac1 as mac1
from aliyunsdkcore.utils import parameter_helper as helper
import requests
import urllib
#
url = 'http://vod.cn-shanghai.aliyuncs.com/?'
accessKeyId = accessKeyId ##修改您的信息
accessKeySecret = accessKeySecret ##修改您的信息
parameters = {
'Title':'xxx',
'FileName':'xxx.m4a',
'FileSize':'3442197',
'Description':'Description',
'Format':'JSON',
'Version':'2017-03-21',
'AccessKeyId':accessKeyId,
'SignatureMethod':'HMAC-SHA1',
'Timestamp':helper.get_iso_8061_date(),
'SignatureVersion':'1.0',
'SignatureNonce':helper.get_uuid()
}

def urlencode(query):
    ret = urllib.urlencode(query)
    ret = ret.replace('+', '%20')
    ret = ret.replace('*', '%2A')
    ret = ret.replace('%7E', '~')
    return ret

def getSignature(parameters,action):
    dic = {'Action':action}
    parameters = dict(parameters, ** dic)
    sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    signString = 'GET&%2F&' + urllib.pathname2url(urlencode(sorted_parameters))
    signature = mac1.get_sign_string(signString, accessKeySecret + '&')
    return signature

#获取视频上传地址和凭证
def getUploadVideoToken(url,parameters):
    action = 'CreateUploadVideo'
    dic = {'Signature':getSignature(parameters,action),'Action':action}
    parameters = dict(parameters, ** dic)
    url = url + '&'.join('%s=%s' % (k, parameters[k]) for k in parameters.keys())
    r = requests.get(url)
    return r.json()

print getUploadVideoToken(url,parameters)