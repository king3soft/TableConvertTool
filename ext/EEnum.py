#枚举的定义和转换
from miniperf import utils_str

#EEnum(男-man-1,女-woman-2)
def custom(cols, sarg, row, j):
    map_datas = sarg.split(',')

    #要剔除空格，请开启
    cols = cols.strip()
    sarg = sarg.strip()

    map_datas = sarg.split(',')
    if len(map_datas) == 0 :
        return (False, 'they are nothing need replace')
    if(cols == "" or cols == None):
        return (True, "")

    #分别有2种情况
    #1.男-man-1  3个参数
    #2.humans-1  2个参数

    #第三个参数，是生成后具体枚举的值，不在此处理 
    mappings = {}
    for item in map_datas:
        arr = item.split('-')
        length = len(arr)
        if length == 2:
            mappings[arr[0]] = arr[0]   
        elif length == 3:
            mappings[arr[0]] = arr[1]


    if type(cols) == type("str"):

        repStr = mappings.get(cols,"None")
        if repStr != "" and repStr != "None":
            cols = repStr
        else:
            return error_msg(cols,row,j) 
    else:
        for e in range(len(cols)) :
            repStr = mappings.get(cols[e],"None")

            if repStr != "" and repStr != "None":
                cols[e] = repStr
            else:
                return error_msg(cols,row,j)


    return (True, cols)


def error_msg(cols,row,j):
   scol = utils_str.col_2_az(j+1)
   return(False,f"【 {cols}  】{row} 行 {j} 列 无法转换！ 请在 {j} 列 2 行内配置EEnum(x-,x-n)")

