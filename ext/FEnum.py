import os
def check(cols, sarg:str):
    print(f'xxxxxxxxxxx{sarg}')
    print(f'{cols}')
    l = len(set(cols))
    r = len(cols)
    # 
    return cols
    if l != r:
        return (False, f'FEnum() 检查失败! {l} != {r}')
    return (True, f'FEnum() 检查成功 {l} == {r}')

def customprcesss(cols, sarg:str):
    pass