# AyiinXd
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinXd >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinXd/blob/main/LICENSE/>.
#
# FROM AyiinXd <https://github.com/AyiinXd/AyiinXd>
# t.me/AyiinXdSupport & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import time


class Log:
    def __init__(self, save_to_file=False, file_name="ayiin.log"):
        self.save_to_file = save_to_file
        self.file_name = file_name

    def info(self, msg):
        print(f"[+]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[INFO]({time.ctime(time.time())}): {msg}\n")

    def error(self, msg):
        print(f"[-]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[ERROR]({time.ctime(time.time())}): {msg}\n")

    def warning(self, msg):
        print(f"[!]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[WARNING]({time.ctime(time.time())}): {msg}\n")
