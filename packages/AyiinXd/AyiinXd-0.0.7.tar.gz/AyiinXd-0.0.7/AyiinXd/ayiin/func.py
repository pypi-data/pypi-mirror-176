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

'''
import asyncio
import shlex
import socket
from typing import Tuple

import dotenv
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from config import Var
from AyiinXd import logs
from AyiinXd.utils.misc import restart


HAPP = None

BRANCH = Var.BRANCH
GIT_TOKEN = Var.GIT_TOKEN
REPO_URL = Var.REPO_URL

XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(Var.HEROKU_API_KEY),
    "https",
    str(Var.HEROKU_APP_NAME),
    "HEAD",
    "AyiinUbot",
]


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL
    try:
        repo = Repo()
        logs.info(f"Git Client Found")
    except GitCommandError:
        logs.info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
        try:
            repo.create_remote("origin", REPO_URL)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(BRANCH)
        try:
            nrs.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -U -r requirements.txt")
        logs.info("Fetched Latest Updates")


def is_heroku():
    return "heroku" in socket.getfqdn()


def heroku():
    global HAPP
    if is_heroku:
        if Var.HEROKU_API_KEY and Var.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
                HAPP = Heroku.app(Var.HEROKU_APP_NAME)
                logs.info(f"Heroku App Configured")
            except BaseException as e:
                logs.error(e)
                logs.info(
                    f"Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku."
                )


async def in_heroku():
    return "heroku" in socket.getfqdn()


async def set_var_value(client, vars, value):
    if await in_heroku():
        if HAPP is None:
            logs.info(
                "Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku"
            )
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
            restart()
        else:
            pass


async def create_premium(client, string_session):
    if Var.SESSION_2 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_2", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_3 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_3", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_4 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_4", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_5 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_5", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_6 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_6", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_7 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_7", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_8 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_8", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_9 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_9", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_10 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_10", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_11 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_11", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_12 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_12", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_13 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_13", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_14 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_14", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_15 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_15", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_16 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_16", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_17 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_17", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_18 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_18", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_19 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_19", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_20 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_20", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_21 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_21", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_22 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_22", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_23 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_23", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_24 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_24", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_25 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_25", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_26 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_26", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_27 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_27", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_28 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_28", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_29 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_29", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_30 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_30", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_31 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_31", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_32 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_32", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_33 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_33", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_34 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_34", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_35 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_35", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_36 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_36", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_37 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_37", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_38 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_38", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_39 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_39", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_40 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_40", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_41 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_41", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_42 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_42", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_43 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_43", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_44 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_44", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_45 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_45", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_46 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_46", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_47 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_47", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_48 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_48", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_49 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_49", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)

    if Var.SESSION_50 != "None":
        pass
    try:
        done = await set_var_value(client, "SESSION_50", string_session)
        if done:
            return True
        else:
            pass
    except BaseException as e:
        logs.info(e)
'''
