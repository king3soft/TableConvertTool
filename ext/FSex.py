import os
def check(cols, sarg:str):
    print(f'xxxxxxxxxxx{sarg}')
    l = len(set(cols))
    r = len(cols)
    if l != r:
        return (False, f'FSex() 检查失败! {l} != {r}')
    return (True, f'FSex() 检查成功 {l} == {r}')

def customprcesss(cols, sarg:str):
    pass