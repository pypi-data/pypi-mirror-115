"""

Микро модуль логирования
Запускается как на сервере, так и на клиенте

"""

import logging
import datetime


logging.basicConfig(
    filename=datetime.datetime.now().strftime("log\\log_server_%Y%m%d.log"),
    format="%(asctime)s - %(levelname)s - %(module)s -  %(message)s ",
    level=logging.DEBUG,
    force=True
)
