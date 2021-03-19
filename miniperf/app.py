import logging
import os
import sys
import time
import datetime
import re
import traceback
from miniperf import extension
from mmgui import App, BrowserWindow, Menu, MenuSeparator

class ColorHandler(logging.StreamHandler):
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)
    def emit(self, record):
        msg_colors = {
            logging.DEBUG: "\x1b[0m",
            logging.INFO: "\x1b[0m",
            logging.WARNING: "\x1b[%s;0m" % self._colors["yellow"],
            logging.ERROR: "\x1b[%s;0m" % self._colors["red"]
        }

        color = msg_colors.get(record.levelno, "\x1b[0m")
        self.stream.write(color)
        super().emit(record)
        self.stream.write("\x1b[0m")

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

console = ColorHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(thread)d %(threadName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.getLogger('').setLevel(logging.DEBUG)


app_name = "TableConvertTool"
app = None
win = None
logger = logging.getLogger("")
version = None
def get_version():
    global version
    if version is None:
        with open(os.path.join(ROOT_DIR, "__init__.py"), encoding="utf8") as f:
            version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
    return version

def move_window(dx, dy):
    win.move_by(dx, dy)


def close_window():
    win.close()


def toggle_maximized_window():
    if win.is_maximized():
        win.show_normal()
    else:
        win.show_maximized()


def show_minimized_window():
    win.show_minimized()


def echo(msg):
    return msg

def rpc_GetFileList():
    xlsx_path = app.get_config("Settting/XLSX_PATH", os.path.join(".", "configs.ini"))
    file_list = extension.rpc_get_file_list(xlsx_path)
    return {"ok" : True, "dat" : file_list}

def rpc_GenCSCodeClick(dat):
    cscode_path = app.get_config("Settting/CSCODE_PATH", os.path.join(".", "configs.ini"))
    csmgr_path = app.get_config("Settting/MGR_PATH", os.path.join(".", "configs.ini"))
    ret = extension.rpc_gen_cscode(dat['path'], cscode_path)
    if ret['ok']:
        ret = extension.rpc_gen_mgrcode(dat['path'], csmgr_path)
    return ret


def on_create(ctx):
    logging.debug("on_create")
    # menus
    menu = Menu()
    # file_menu = Menu(title="File")
    #file_menu.append(Menu(title="Open", on_click=lambda e: logging.debug("open file")))
    #file_menu.append(MenuSeparator())
    # file_menu.append(Menu(title="Exit", on_click=lambda e: app.exit()))
    # menu.append(file_menu)

    global win
    win = BrowserWindow({
        "title": app_name,
        "width": 1200,
        "height": 800,
        "dev_mode": False,
        #"frameless": True,
        "menu": menu
    })
    win.webview.bind_function("echo", echo)
    win.webview.bind_function("toggle_maximized_window", toggle_maximized_window)
    win.webview.bind_function("show_minimized_window", show_minimized_window)
    win.webview.bind_function("close_window", close_window)
    win.webview.bind_function("move_window", move_window)
    import FHelper
    FHelper.app = app
    extension.registered_webview(win.webview)

    # rpc_CheckTableClick
    win.webview.bind_function("rpc_CheckTableClick", lambda dat: extension.rpc_CheckTableClick(dat))
    win.webview.bind_function("rpc_GetFileList", rpc_GetFileList)
    # rpc_GenTabFileClick
    win.webview.bind_function("rpc_GenTabFileClick", lambda dat: extension.rpc_GenTabFileClick(dat))
    # rpc_GenCSAndTabCodeClick
    win.webview.bind_function("rpc_GenCSAndTabCodeClick", lambda dat: extension.rpc_GenCSAndTabCodeClick(dat))
    # rpc_CommitCSAndTabCodeClick
    win.webview.bind_function("rpc_CommitCSAndTabCodeClick", lambda dat: extension.rpc_CommitCSAndTabCodeClick(dat))

    win.webview.bind_function("onFolderChange", lambda dat: extension.rpc_open_folder(dat))
    # rpc_DefaultSetting
    win.webview.bind_function("rpc_DefaultSetting", lambda dat: extension.rpc_DefaultSetting(app))
    # rpc_OpenXlsxFileClick
    win.webview.bind_function("rpc_OpenXlsxFileClick", lambda dat: extension.rpc_OpenXlsxFileClick(dat))
    # rpc_CommitFileClick
    win.webview.bind_function("rpc_CommitFileClick", lambda dat: extension.rpc_CommitFileClick(dat))
    # rpc_CommitAllFilesClick
    win.webview.bind_function("rpc_CommitAllFilesClick", lambda dat: extension.rpc_CommitAllFilesClick(dat))
    # rpc_ConvertAllFilesClick
    win.webview.bind_function("rpc_ConvertAllFilesClick", lambda dat: extension.rpc_ConvertAllFilesClick(dat))
    win.webview.bind_function("rpc_HelpButtonClick", lambda dat: extension.rpc_HelpButtonClick(dat))



    # event listeners
    win.webview.register_event_listener("on_url_changed", lambda e: logging.debug("on_url_changed, url=%s" % e.data))
    # win.webview.register_event_listener("on_page_load_finished", lambda e: logging.debug("cookie %s" % win.webview.get_cookie(".baidu.com", "BAIDUID")))
    win.webview.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "index.html"))
    # app.set_main_window(win.get_main_window())

    win.show()


def on_destroy(ctx):
    logging.debug("on_destroy")
    global win
    if win:
        win.close()
        win = None

def main():
    data_dir = os.path.abspath(os.path.join(".", "data"))
    log_dir = os.path.join(data_dir, "log")
    report_dir = os.path.join(data_dir, "report")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    global app
    icon_file=os.path.abspath(os.path.join(ROOT_DIR, "ui", "res", "img", "icon.png")),
    splash_file=os.path.abspath(os.path.join(ROOT_DIR, "ui", "res", "img", "splash.png")),
    splash_text="%s v%s\n\nLoading..." % (app_name, get_version()),
    icon_file=icon_file,
    app = App(headless=False,
              configs_file=os.path.abspath(os.path.join(".", "configs.ini")),
              log_file=os.path.abspath(os.path.join(log_dir, '%s_%s.log' % (app_name, datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y_%m_%d_%H%M%S')))),
              )
    # add ext dir to path
    ext = app.get_config("Ext/Ext_PATH", "./ext")
    sys.path.append(os.path.abspath(ext))

    sys.path.append(os.path.join(ROOT_DIR, 'ext'))

    app.on("create", on_create)
    app.on("destroy", on_destroy)
    exit_code = app.run()
    logging.debug("sys.exit code=%d" % exit_code)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
