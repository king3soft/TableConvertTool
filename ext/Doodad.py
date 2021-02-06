from openpyxl.worksheet.worksheet import Worksheet

#自定义检查触发范围
def check(ws:Worksheet, ws_dict:dict):
    for k, v in ws_dict.items():
        print(k, v)
    return (True, '')

if __name__ == "__main__":
    pass

