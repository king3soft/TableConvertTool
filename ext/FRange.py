import os
def check(cols, sarg:str):
    l = len(set(cols))
    r = len(cols)
    if l != r:
        return (False, f'FRange() 检查失败! {l} != {r}')
    return (True, f'FRange() 检查成功 {l} == {r}')