from __future__ import absolute_import

import os
import shutil

# Find the best implementation available
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import flask

from .forms import ImageClassificationDatasetForm
#from digits.utils.forms import fill_form_if_cloned, save_form_to_job


blueprint = flask.Blueprint(__name__, __name__)


@blueprint.route('/new', methods=['GET'])
def new():
    """
    Returns a form for a new ImageClassificationDatasetJob
    """
    form = ImageClassificationDatasetForm()

    # Is there a request to clone a job with ?clone=<job_id>
    #fill_form_if_cloned(form)

    return flask.render_template('datasets/images/classification/new.html', form=form)

