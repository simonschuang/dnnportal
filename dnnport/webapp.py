from __future__ import absolute_import

import os

import flask
from flask.ext.socketio import SocketIO
from gevent import monkey
monkey.patch_all()

from .config import config_value  # noqa
from dnnport import utils  # noqa
from dnnport.utils import filesystem as fs  # noqa
from dnnport.utils.store import StoreCache  # noqa
import dnnport.scheduler  # noqa

# Create Flask, Scheduler and SocketIO objects

app = flask.Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True
# Disable CSRF checking in WTForms
app.config['WTF_CSRF_ENABLED'] = False
# This is still necessary for SocketIO
app.config['SECRET_KEY'] = os.urandom(12).encode('hex')
app.url_map.redirect_defaults = False
app.config['URL_PREFIX'] = url_prefix
socketio = SocketIO(app, async_mode='gevent', path='/socket.io')
app.config['store_cache'] = StoreCache()
app.config['store_url_list'] = config_value('model_store')['url_list']
scheduler = dnnport.scheduler.Scheduler(config_value('gpu_list'), True)

# Register filters and views

app.jinja_env.globals['server_name'] = config_value('server_name')
app.jinja_env.globals['server_version'] = dnnport.__version__
app.jinja_env.globals['caffe_version'] = config_value('caffe')['version']
app.jinja_env.globals['caffe_flavor'] = config_value('caffe')['flavor']
app.jinja_env.globals['dir_hash'] = fs.dir_hash(
    os.path.join(os.path.dirname(dnnport.__file__), 'static'))
app.jinja_env.filters['print_time'] = utils.time_filters.print_time
app.jinja_env.filters['print_time_diff'] = utils.time_filters.print_time_diff
app.jinja_env.filters['print_time_since'] = utils.time_filters.print_time_since
app.jinja_env.filters['sizeof_fmt'] = utils.sizeof_fmt
app.jinja_env.filters['has_permission'] = utils.auth.has_permission
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

import dnnport.views  # noqa
app.register_blueprint(dnnport.views.blueprint,
                       url_prefix=url_prefix)
import dnnport.dataset.views  # noqa
app.register_blueprint(dnnport.dataset.views.blueprint,
                       url_prefix=url_prefix+'/datasets')
import dnnport.dataset.generic.views  # noqa
app.register_blueprint(dnnport.dataset.generic.views.blueprint,
                       url_prefix=url_prefix+'/datasets/generic')
import dnnport.dataset.images.views  # noqa
app.register_blueprint(dnnport.dataset.images.views.blueprint,
                       url_prefix=url_prefix+'/datasets/images')
import dnnport.dataset.images.classification.views  # noqa
app.register_blueprint(dnnport.dataset.images.classification.views.blueprint,
                       url_prefix=url_prefix+'/datasets/images/classification')
import dnnport.dataset.images.generic.views  # noqa
app.register_blueprint(dnnport.dataset.images.generic.views.blueprint,
                       url_prefix=url_prefix+'/datasets/images/generic')
import dnnport.model.views  # noqa
app.register_blueprint(dnnport.model.views.blueprint,
                       url_prefix=url_prefix+'/models')
import dnnport.model.images.views  # noqa
app.register_blueprint(dnnport.model.images.views.blueprint,
                       url_prefix=url_prefix+'/models/images')
import dnnport.model.images.classification.views  # noqa
app.register_blueprint(dnnport.model.images.classification.views.blueprint,
                       url_prefix=url_prefix+'/models/images/classification')
import dnnport.model.images.generic.views  # noqa
app.register_blueprint(dnnport.model.images.generic.views.blueprint,
                       url_prefix=url_prefix+'/models/images/generic')
import dnnport.pretrained_model.views  # noqa
app.register_blueprint(dnnport.pretrained_model.views.blueprint,
                       url_prefix=url_prefix+'/pretrained_models')
import dnnport.store.views  # noqa
app.register_blueprint(dnnport.store.views.blueprint,
                       url_prefix=url_prefix+'/store')


def username_decorator(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        this_username = flask.request.cookies.get('username', None)
        app.jinja_env.globals['username'] = this_username
        return f(*args, **kwargs)
    return decorated

for endpoint, function in app.view_functions.iteritems():
    app.view_functions[endpoint] = username_decorator(function)

# Setup the environment

scheduler.load_past_jobs()
