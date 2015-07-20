from flask import render_template
import yaml


def start_page(g, request):
    context = dict()
    with open('api_doc/api_documentation.yaml', 'r') as stream:
        context['documentation'] = yaml.load(stream)

    return render_template('api/start_page.html', **context)
