from flask import render_template
from flask import g

import yaml


def start_page(request):
    context = dict()
    with open('api/api_documentation.yaml', 'r') as stream:
        context['documentation'] = yaml.load(stream)

    return render_template('api/start_page.html', **context)
