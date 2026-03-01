# SPDX-FileCopyrightText: 2026 Daniel Feito-Pin <danielfeitopin+github@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pathlib

FETCH_DATA: bool = True
CREATE_TABLES: bool = True

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
DATA_DIR: pathlib.Path = BASE_DIR / 'data'
DB_PATH: str = "sqlite:///notasfic.db"