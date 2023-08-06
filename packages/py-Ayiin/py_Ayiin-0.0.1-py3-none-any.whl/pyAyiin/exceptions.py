# AyiinXd - Library 
# Copyright (C) 2021-2022 AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinXd/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/AyiinXd/AyiinXd/blob/main/LICENSE>.

"""
Exceptions which can be raised by AyiinXd Itself.
"""


class AyiinXdError(Exception):
    ...


class PyrogramMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(AyiinXdError):
    ...
