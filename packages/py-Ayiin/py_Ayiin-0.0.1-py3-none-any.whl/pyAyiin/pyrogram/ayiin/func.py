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

import dotenv
import logging

from .hosting import where_hosted


logs = logging.getLogger(__name__)

HOSTED_ON = where_hosted()


async def set_var(HAPP, vars, value, started):
    if HOSTED_ON == "Heroku":
        heroku_config = HAPP.config()
        if vars not in heroku_config:
            heroku_config[vars] = value
            logs.info(f"Berhasil Menambahkan Vars {vars}")
            return True
        else:
            pass
    else:
        path = dotenv.find_dotenv(".env")
        if not path:
            logs.info(".env file not found.")
        if not dotenv.get_key(path, vars):
            dotenv.set_key(path, vars, value)
            logs.info(f"Berhasil Menambahkan var {vars}")
            started()
        else:
            pass


async def del_var(HAPP, vars, started):
    if HOSTED_ON == "Heroku":
        heroku_config = HAPP.config()
        if vars in heroku_config:
            del heroku_config[vars]
            logs.info(
                f"Berhasil Menghapus Vars {vars}",
            )
            return True
        else:
            pass
    else:
        path = dotenv.find_dotenv(".env")
        if not path:
            logs.info(".env file not found.")
        if dotenv.get_key(path, vars):
            dotenv.unset_key(path, vars)
            logs.info(
                f"Berhasil Menghapus Vars {vars}",
            )
            started()
        else:
            pass
