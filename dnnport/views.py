
from flask import Blueprint, render_template


blueprint = Blueprint(__name__, __name__)


@blueprint.route('/', methods=['GET'])
def home(tab=2):
    new_dataset_options = {
            'Images': {
                'image-classification': {
                    'title': 'Classification',
                    'url': flask.url_for(
                        'dnnport.dataset.images.classification.views.new'),
                },
            },
        }
    new_model_options = {}
    load_model_options = {}
    return render_template(
        'home.html',
        new_dataset_options = new_dataset_options,
        new_model_options = new_model_options,
        load_model_options = load_model_options,
    )
