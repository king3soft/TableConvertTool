import os
def check(cols, sarg:str,j:int):
    l = len(set(cols))
    r = len(cols)
    if l != r:
        return (False, f'FUnique() 检查失败! {l} != {r}')
    return (True, f'FUnique() 检查成功 {l} == {r}')