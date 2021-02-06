import os
import FHelper
import traceback
def check(cols, sarg:str):
    try:
        args = sarg.split(',')
        tab_name = args[0]
        tab_field = args[1]
        succeed, table, msg = FHelper.get_table(tab_name)
        if not succeed:
            return (False, msg)

        for e in cols:
            if e not in table[tab_field]:
                return (False, f'FLINK({sarg}) 检查失败! {e} not in {sarg}')

        return (True, f'FRange() 检查成功')
    except Exception as e:
        traceback.print_exc()
        return (False, f'FLINK({sarg}) 检查失败! \n{traceback.format_exc()}')
