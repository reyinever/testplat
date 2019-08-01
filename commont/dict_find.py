
def dict_get(dictObj,key,default=''):
    """
    dict:嵌套字典
    key: 要查找的对象
    default:找不到时返回的默认值
    """
    tmp=dictObj.copy()
    for k,v in tmp.items():
        if k==key:
            return v
        else:
            if isinstance(v,dict):
                ret=dict_get(v,key,default)
                return ret
    return default


if __name__ == '__main__':
    dicttest={"result":{"code":"110002","msg":"设备设备序列号或验证码错误"}}
    key='msg'
    print(dict_get(dicttest,key))
