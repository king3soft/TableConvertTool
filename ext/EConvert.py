
from miniperf import utils_str

#sarg (1-男,2-女) 
def custom(cols, sarg, row, j):
    # 按sarg 映射转换字符串

    #要剔除空格，请开启
    cols = cols.strip()
    sarg = sarg.strip()

    map_datas = sarg.split(',')
    if len(map_datas) == 0 :
        return (False, 'they are nothing need replace')


    if(cols == "" or cols == None):
        return (True, "")

    mappings = {}
    for item in map_datas:
        arr = item.split('-')
        mappings[arr[1]] = arr[0]

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
   return(False,f"【 {cols}  】{row} 行 {scol} 列 无法转换！ 请在 {scol} 列 2 行内配置EConvert(x-{cols},x-n)")

