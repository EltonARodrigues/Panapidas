# logger.py
#
# Copyright 2026 Elton de Andrade Rodrigues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

import logging
import re
import sys

from panapidas import const

class ProjectFileFilter(logging.Filter):
    """The path name of the package."""

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        record.packagename = re.search(r'(?=panapidas)[\s\S]*', record.pathname).group(0)
        return True


logger = logging.getLogger()
format = "%(packagename)s:%(lineno)d %(levelname)8s: %(funcName)s(): %(message)s"

if const.PROFILE == "development":
    logging.basicConfig(
        format=format,
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format=format,
        level=logging.INFO,
    )

logger.handlers[0].addFilter(ProjectFileFilter())
