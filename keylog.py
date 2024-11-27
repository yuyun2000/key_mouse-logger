import pythoncom
import pyWinhook as pyHook
import logging
import time

# 获取当前年月信息并格式化为字符串，比如 "2023_03"
current_month = time.strftime('%Y_%m')

# 更新日志文件名称以包含当前月份信息
log_filename = f'key_mouse_log_{current_month}.txt'

# 配置日志记录，同时输出到文件和控制台
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# 设置记录鼠标移动事件的最小时间间隔（秒）
move_interval = 0.1
last_move_time = 0


def on_keyboard_event(event):
    logging.info(f'Key {event.Key}')
    return True


def on_mouse_event(event):
    global last_move_time
    current_time = time.time()

    if event.MessageName == 'mouse move':
        # 只记录一定时间间隔内的事件
        if current_time - last_move_time > move_interval:
            logging.info(f'Mouse moved to ({event.Position[0]}, {event.Position[1]})')
            last_move_time = current_time
    elif event.MessageName.startswith('mouse '):
        if current_time - last_move_time > move_interval:
            logging.info(f'{event.MessageName} at ({event.Position[0]}, {event.Position[1]})')
            last_move_time = current_time


    return True


# 创建钩子管理对象
hm = pyHook.HookManager()

# 监视键盘事件
hm.KeyDown = on_keyboard_event
hm.HookKeyboard()

# 监视鼠标事件
hm.MouseAll = on_mouse_event
hm.HookMouse()

# 循环获取消息
pythoncom.PumpMessages()
