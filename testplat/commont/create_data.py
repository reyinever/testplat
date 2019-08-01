import os
from commont.public_var import unique_number_path
import pickle
from commont.Log import *
import random
import string


def get_unique_number(unique_number_path=unique_number_path,start_number=1):
    """获取唯一数"""
    try:
        # 从文件中读取唯一数
        # 如果文件不为空,进行读取
        if os.path.getsize(unique_number_path)>0:
            with open(unique_number_path,'rb')as fp:
                data=pickle.load(fp)
                unique_number=data.get('unique_number','')
                if not unique_number:
                    unique_number=start_number
                    next_unique_number=start_number+1
                else:
                    next_unique_number=unique_number+1
                # print(unique_number)
        else:
            # 设置唯一数的初始值
            unique_number=start_number
            # 设置下一个唯一数的值
            next_unique_number=unique_number+1
        # 构造要保存的数据格式
        next_data = {'unique_number': next_unique_number}
        # 把下一个唯一数存入文件
        with open(unique_number_path,'wb') as fp:
            pickle.dump(next_data,fp)
        info('获取唯一数变量值:%s,存储下一个唯一数据变量值:%s'%(unique_number,next_unique_number))
        return unique_number
    except Exception as e:
        info("获取唯一数变量值失败，获取的唯一数变量是%s,异常原因如下：%s" %(unique_number,e))


def get_digit(start_num=100,end_num=1000):
    """生成 start_num 到 end_num 之间的数字"""
    try:
        if start_num>end_num:
            start_num,end_num=end_num,start_num
        return random.randint(start_num,end_num)
    except Exception as e:
        info('生成数字异常:',e)
        return None


def get_str(lenth=9):
    """生成 指定长度的字符串"""
    try:
        s=random.sample(string.ascii_letters,lenth)
        # print(s)
        random.shuffle(s)
        s="".join(s)
        return s
    except Exception as e:
        info('生成字符串异常:',e)
        return None


def get_letter_digit(lenth=9):
    """生成指定长度的字母、数字组合字符串"""
    try:
        s_start=get_str(1)
        mid=int((lenth-1)/2)
        s_mid=random.sample(string.ascii_letters,mid)
        end=lenth-1-mid
        s_end=random.sample(string.digits,end)
        s_mid_end=s_mid+s_end
        random.shuffle(s_mid_end)
        s_mid_end="".join(s_mid_end)
        return s_start+s_mid_end
    except Exception as e:
        info('生成字母、数字组合的字符串异常：',e)
        return None


if __name__ == '__main__':
    # print(get_unique_number(unique_number_path))
    # print(get_str(5))
    print(get_letter_digit())
