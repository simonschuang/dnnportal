# from __future__ import absolute_import

import os
from flask import Flask


def register_blueprints(app):
    """Register all blueprint modules
    """
    import dnnport.views  # noqa
    app.register_blueprint(dnnport.views.blueprint)

    return None


# Create Flask, Scheduler and SocketIO objects
app = Flask("dnnport")

app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = os.urandom(12).encode('hex'),
))

register_blueprints(app)
