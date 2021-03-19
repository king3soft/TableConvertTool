import logging
import os
import time
import traceback
import shutil
import sys
import threading
import datetime
import time
import glob
import wcwidth
import importlib
import subprocess
import re
import csv


class Header(object):
    def __init__(self, _comment, _filed, _type, _tags):
      
        _map = {"int": "0", "string": ""}
        self.Comment = f"{_comment}".replace("\r\n", "")
        self.Filed = f"{_filed}"
        self.FiledType = f"{_type}"
        self.Default = _map.get(self.FiledType, "")
        self.Tags = f"{_tags}"

#('List', 'Item', 'Items', 'int', 'Count', 'List<Item>')    --list 
#('Array', 'Item', 'xiao', 'int', 'Count', 'Item[]')        --Array
#('string', 'string', 'talent', '', '', 'string')           --内置值类型
#('Item', 'Item', 'item', 'int', 'ID', 'Item')              --自定义数据类型
#('enum', 'ESex', 'sex', '', '', 'ESex')                 --枚举类型
def analysis_Class(typeStr:str,filedStr:str) :
    farr = filedStr.split('.')
    att1_name = farr[0]
    att2_name =  len(farr) > 1 and farr[1] or ""

    arr = typeStr.split('.')
    att1_type = arr[0]
    att2_type = len(arr) > 1 and arr[1]  or ""
    # 检查是不是泛型
    dt_type = 'none'#第一类型(如果不是内置类型需要创建)
    T_type = 'none' #第二类型，包括泛型的类型(如果不是内置类型需要创建)
    sindex = att1_type.find('<')
    eindex = att1_type.find('>')


    if sindex != -1 and eindex != -1:
        #泛型List
        dt_type = att1_type[0:sindex]
        T_type = att1_type[sindex+1:eindex]
    else:
        sindex = att1_type.find('[')
        eindex = att1_type.find(']')
        if sindex != -1 and eindex != -1:
            #Array
            dt_type = 'Array'
            T_type = att1_type[0:sindex]
        elif arr[0] == "enum":
            dt_type = "enum"
            T_type = att2_type
            att1_type = att2_type
            att2_type = ""

        else:
            dt_type = att1_type
            T_type = att1_type

    return dt_type, T_type,att1_name,att2_type,att2_name,att1_type


csharp_types        = ["int","float","double","string","bool","List","Array","Queue","Stack"]
csharp_simpleBase   = ["int","float","double","string","bool"]
csharp_Tcontainer   = ["Array","List","Queue","Stack"]
csharp_custom_class = {}

def add_custom_class(calName,attType,attName,inherit):
   
    classVal = csharp_custom_class.get(calName,"None")
    if classVal == "None" :
        classVal = {"__className":calName,"attribute":{},"inherit":False}

        csharp_custom_class[calName] = classVal
    if inherit :
        classVal["inherit"] = True
        
    classVal["attribute"][attName] = attType;


def gen_custom_class(data) :
    #data = {'DropItem': {'__className': 'DropItem', 'attribute': {'name': 'string', 'id': 'int'},'inherit':False}}
    inherit   = data["inherit"]

    template_1 = "\n\t\tpublic class __NAME__ : TableFileRow\n\t\t{\n"
    template_4 = "\n\t\tpublic class __NAME__ \n\t\t{\n"
    template_2 = "\t\t\tpublic __TYPE__  __NAME__;\n"
    template_3 = "\t\t\t\t__NAME__ = Get___TYPE__(cellStrs[int.Parse(indexStrs[__INDEX__])], \"\");\n"

    class_str = (inherit and template_1 or template_4).replace("__NAME__",data["__className"])

    attribute = data["attribute"]
    
    #属性部分
    setValuesStrs = ""
    index = 0
    for key in attribute.keys() :
        str2 = template_2.replace("__NAME__",key)
        str2 = str2.replace("__TYPE__",attribute[key])
        class_str += str2

        #赋值代码
        setValue = template_3.replace("__NAME__",key)
        setValue = setValue.replace("__TYPE__",attribute[key])
        setValue = setValue.replace("__INDEX__",str(index))
        index += 1
        setValuesStrs += setValue

    #方法部分
    if inherit :
        class_str += "\n\t\t\tpublic override void Parse(string[] cellStrs, string[] indexStrs)\n\t\t\t{\n"
        class_str += setValuesStrs
        class_str += "\n\t\t\t}\n"
       
    class_str += "\n\t\t}\n"    
    return  class_str

def instance_custom_class(data,history,getvalue,c_col) :

    template_1 = '\t\t\t__NAME__ = new __TYPE__();\n'
    template_3 = '\t\t\t__NAME__.__FILED__ = __VALUE__;\n'
    
    type_first  = data[0]#List<T>的List
    type_second = data[1]#List<T>的T
    name_first  = data[2]#List<T> m_list 的 mlist
    type_third  = data[3]#T 属性的类型
    name_third  = data[4]#T 属性名

    #有多种形态
    #('List', 'int', 'shoots', '', '', 'List<int>')
    #('List', 'DropItem', 'items1', 'int', 'id', 'List<DropItem>')    
    #('Array', 'int', 'arr', 'int', 'id', 'int[]')
    #('DogItem', 'DogItem', 'dog_1', 'int', 'id', 'DogItem')    
    
    filed = data[4]

    instance_key = f"{type_first}_{type_second}_{name_first}"

    item_values = history.get(instance_key,"None")

    cType = type_first in csharp_Tcontainer and 1 or 2

    #======================初始化===================
    parser_str  = ""#初始化
    parser_str2 = ""#赋值
    if item_values == "None" :

        if cType == 1:
            #数组,# 泛型集合
            #('Array', 'int', 'arr', 'int', 'id', 'int[]')
             #('List', 'DropItem', 'items1', 'string', 'name', 'List<DropItem>')
            #print("Array ,List 在赋值时在初始化")
            item_values = [] 
        else:
            item_values = True 
            #自定义类
            #('DogItem', 'DogItem', 'dog_1', 'int', 'id', 'DogItem')
            parser_str = template_1.replace("__NAME__", name_first)
            parser_str = parser_str.replace("__TYPE__", type_second)

           
        #记录初始化
        history[instance_key] = item_values

    #=====================赋值=====================

    if cType == 2 :
        #给对象直接赋值
        parser_str2 = template_3.replace("__NAME__", name_first)
        if name_third != "" :
            #有第二个属性
            parser_str2 = parser_str2.replace("__FILED__", name_third)
        else:
            parser_str2 = parser_str2.replace(".__FILED__", "")

        parser_str2 = parser_str2.replace("__VALUE__", getvalue)
    else:
        #按长度记录数据
        if type_second in csharp_simpleBase:
            #子类型是基础类型
            item_values.append(str(c_col))#记录index
        else:
            #子类型是类，递增
            leng = len(item_values)

            if leng == 0 :
                class_msg = {}
                item_values.append(class_msg)
            else:
               class_msg =  item_values[leng-1]

               hadVale = class_msg.get(name_third,"None")
               if hadVale != "None":
                   #已经记录了,需要继续往后扩展
                   class_msg = {}
                   item_values.append(class_msg)

            class_msg[name_third] = str(c_col)  #记录index 

    return  parser_str + parser_str2


template_list_value   = "__FILED__ = Get_@_Value<__T__>(cellStrs, \"Get___T__|__MSG__\");\n\t\t\t"
template_list_class   = "__FILED__ = Get_@<__T__>(cellStrs, \"__MSG__\",\"\");\n\t\t\t"

def set_custom_class(history):

    # {
    #     'Item_Item_item': True, 
    #     'OOP_OOP_oop': True, 
    #     'List_int_shoots': ['9', '10', '11', '12'], 
    #     'List_Item_Items': 
    #     [
    #         {'ID': '13', 'Inventory': '14', 'Count':'15', 'Weight': '16'}, 
    #         {'ID': '17', 'Inventory': '18', 'Count':'19', 'Weight': '20'}, 
    #         {'ID': '21', 'Inventory': '22', 'Count':'23', 'Weight': '24'}
    #     ]
    # }
    list_value_template = [] 
    for key ,val in history.items():
        if val == True :continue

        line = ""
        #复杂类型 key = List_int_shoots
        arr = key.split("_")

        type_first  = arr[0]
        type_second = arr[1]
        filename    = arr[2]
        line =''
        if type_first in csharp_Tcontainer :
        #list 语法
            if type_second in csharp_simpleBase:
             #直接 Add
                line = template_list_value.replace("__FILED__",filename)
                line = line.replace("@",type_first)
                line = line.replace("__T__",type_second)
                line = line.replace("__MSG__",",".join(val))
            else:
                #class类型
                line = template_list_class.replace("__FILED__",filename)
                line = line.replace("@",type_first)
                line = line.replace("__T__",type_second)
                msgstr = ""
                for item in val:
                    if msgstr != "":
                        msgstr += "|"

                    msgstr +=  ",".join(item.values())

                line = line.replace("__MSG__",msgstr) 

        list_value_template.append(line)           

    return list_value_template


#enumName     ESex
#attributes   [man,1]
csharp_custom_enum = {}
def  add_custom_enum(enumName,attributes):
    enumVal = csharp_custom_enum.get(enumName,"None")
    if enumVal == "None" :
        enumVal = {"__enumName":enumName,"attribute":{}}
        csharp_custom_enum[enumName] = enumVal

    enumVal["attribute"][attributes[0]] = attributes[1]
           
#{'ESex': {'__enumName': 'ESex', 'attribute': {'man': '1', 'woman': '2'}}}           
def gen_custom_enum(data):

    template_1 = "\n\t\tpublic enum __NAME__ \n\t\t{\n\t\t\tInvalid = 0,//空配置默认值\n"
    template_2 = "\t\t\t__NAME__ = __Value__,\n"
    enum_str = template_1.replace("__NAME__",data["__enumName"])

    attribute = data["attribute"]
    
    for key in attribute.keys() :
        str2 = template_2.replace("__NAME__",key)
        str2 = str2.replace("__Value__",attribute[key])
        enum_str += str2
       
    enum_str += "\n\t\t}\n"   

    return  enum_str

def get_enum_value(enumName,attribute):
    enumVal = csharp_custom_enum.get(enumName,"None")
    if enumVal != "None" :
        return enumVal["attribute"][attribute]