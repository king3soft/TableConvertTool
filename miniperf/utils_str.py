import re

#把数字转换成  a-z
AZ = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
def col_2_az(col_int):

    col_str=''
    if(col_int<=26):
        col_str=AZ[col_int-1]
    elif(col_int < 702):
        col_int=col_int-27
        col_str=AZ[int(col_int/26)]+AZ[int(col_int%26)]
    elif(col_int==702):
        col_str='ZZ'
    else:
        col_int=col_int-703
        col_str=AZ[int(col_int/676)]+AZ[int(col_int/26)%26]+AZ[col_int%26]

    return(col_str)

def isNoneOrEmpty(str):    
    return str == None or str == ""

def tag_parser(tag):
    tag = tag.replace(' ', '')
    if '(' not in tag:
        return (tag, '')
    else:
        #re_funargs = re.compile('(?P<func>F[a-zA-Z0-9_]+)\((?P<args>[^)]*)\)')
        re_funargs = re.compile('(?P<func>[F|E]?[a-zA-Z0-9_]+)\((?P<args>[^)]*)\)')
        m = re.match(re_funargs, tag)
        return (m['func'], m['args'])


#从tags中获取指定方法的参数
def get_fun_args(tags,funName):
    tag_list = tags.split('|')
    for tag in tag_list:
        func, args = tag_parser(tag)
        if func == funName :
            return args.split(",")
