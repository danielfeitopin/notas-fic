# SPDX-FileCopyrightText: 2026 Daniel Feito-Pin <danielfeitopin+github@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Flask
from app.routes import create_routes
from app.utils.db import SESSION

def create_app():
    app = Flask(__name__)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SESSION.remove()


    create_routes(app)
    return app