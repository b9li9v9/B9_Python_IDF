from datetime import datetime
import time
from B9_UserConfig import UserConfig

class Logger():
    temptime = str(datetime.fromtimestamp(int(time.time())))

    # 写入日志
    @classmethod
    def write_log(cls,message):
        print(f"{cls.temptime} {message}")
        with open(UserConfig.BuildLogPath, 'a', encoding='UTF-8') as file:
            file.write(f"{cls.temptime} {message}")

    # 清空日志
    @classmethod
    def clear_log(cls):
        with open(UserConfig.BuildLogPath, 'w',encoding='utf-8') as file:
            file.truncate(0)

