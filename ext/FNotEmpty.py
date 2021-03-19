from miniperf import utils_str

def check(cols, sarg, j):

    for i in range(len(cols)):
    	if i <= 4: continue
    	if(cols[i] == "None" or cols[i] == None):
    		return error_msg(cols,i+1,j)
    return (True,"")


def error_msg(cols,i,j):
   scol = utils_str.col_2_az(j+1)
   return(False,f"{i} 行 {scol} 列 为空！ FNotEmpty 禁止列存在空")