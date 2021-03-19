import os

def check(cols, sarg:str,j:int):
    arg1 = sarg.split(',')[0]
    for e in cols:
        if not e.startswith(arg1):
            return (False, f'FStartWith({sarg}) 检查失败! {e}')
    return (True, f'FStartWith({sarg}) 检查成功 {e}')