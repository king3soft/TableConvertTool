import importlib
import os
import re
from miniperf import utils_str


#E开头的扩展文件
def custom(row,j,extend,taglist,cols):
   
    tags = taglist.get(j,"None")
    if tags == "None" :
        #解析配置函数
        tags = []
        tag_list = extend.split('|')
        for tag in tag_list:
            func, args = utils_str.tag_parser(tag)
            tags.append((j, func, args))
        
        taglist[j] = tags
    #执行    
    for i, func, args in tags:
        if func[:1] == "E":
            modulename = func
            spec = importlib.util.find_spec(modulename)
            if spec:
                module = importlib.reload(importlib.__import__(modulename))
                if module:
                    ok, result = module.custom(cols, args,row,j)
                    if ok:
                        cols = result#更新
                    else:
                         return (False, f"{result}")
        # else if func[:1]  = "C":   
        # 记得在tag_parser正则表达式 E|F处加上|C,否则报错

    return (True,cols) #返回结果  