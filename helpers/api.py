from flask import render_template
import yaml


def start_page(g, request):
    context = dict()
    with open('helpers/api_documentation.yaml', 'r') as stream:
        context['documentation'] = yaml.load(stream)

    return render_template('api/start_page.html', **context)


def top_prefixes(g, request):
    # curl http://127.0.0.1:5000/api/v1.0/top_prefixes\?limit_prefixes=10\&start_time\=2015-07-13T14:00\&end_time\=2015-07-14T14:00
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit_prefixes = int(request.args.get('limit_prefixes', 0))
    net_masks = request.args.get('net_masks', '')
    exclude_net_masks = request.args.get('exclude_net_masks', False)

    data = {
        'result': {
            'top_prefixes': db.aggregate_per_prefix(
                start_time, end_time,
                limit=limit_prefixes,
                net_masks=net_masks,
                exclude_net_masks=exclude_net_masks),
        },
        'parameters': {
            'limit_prefixes': limit_prefixes,
            'start_time': start_time,
            'end_time': end_time,
            'net_masks': net_masks,
            'exclude_net_masks': exclude_net_masks,
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data


def top_asns(g, request):
    # curl http://127.0.0.1:5000/api/v1.0/top_asns\?start_time=2015-07-13T14:00\&end_time=2015-07-14T14:00
    db = getattr(g, 'db')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    data = {
        'result': {
            'top_asns': db.aggregate_per_as(start_time, end_time),
        },
        'parameters': {
            'start_time': start_time,
            'end_time': end_time,
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data

def _variables_post(g, request):
    # curl -i -H "Content-Type: application/json" -X POST -d '{"name": "test", "content": "this_is_a_test", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables
    db = getattr(g, 'db')

    name = request.json.get('name')
    content = request.json.get('content')
    category = request.json.get('category')
    extra_vars = request.json.get('extra_vars')

    db.put_variables(name, content, category, extra_vars)

    data = {
        'result': {
            'variable': db.get_variable(category, name),
        },
        'parameters': {
            'name': name,
            'content': content,
            'category': category,
            'extra_vars': str(extra_vars),
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data

def _variables_get(g, request):
    db = getattr(g, 'db')
    data = {
        'result': {
            'variables': db.get_variables(),
        },
        'parameters': {},
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data

def variables(g, request):
    if request.method == 'GET':
        return _variables_get(g, request)
    elif request.method == 'POST':
        return _variables_post(g, request)

def _api_variables_var_id_get(g, request, name):
    db = getattr(g, 'db')
    data = {
        'result': {
            'variable': db.get_variable(name),
        },
        'parameters': {
            'name': name,
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data

def api_variables_name(g, request, category, name):
    db = getattr(g, 'db')

    if request.method == 'GET':
        result = db.get_variable(category, name)
    elif request.method == 'PUT':
        # curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "test", "content": "this_is_a_testa", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables/test
        variable = db.get_variable(category, name)
        new_name = request.json.get('name', variable['name'])
        new_content = request.json.get('content', variable['content'])
        new_category = request.json.get('category', variable['category'])
        new_extra_vars = request.json.get('extra_vars', variable['extra_vars'])
        db.update_variable(name, category, new_name, new_content, new_category, new_extra_vars)
        result = db.get_variable(new_category, new_name)
    elif request.method == 'DELETE':
        db.delete_variable(category, name)
        result = 1

    data = {
        'result': {
            'variable': result,
        },
        'parameters': {
            'name': name,
            'categories': category,
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data


def variables_category(g, request):
    db = getattr(g, 'db')
    data = {
        'result': {
            'categories': db.get_categories(),
        },
        'parameters': {},
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data


def variables_filter_by_category(g, request, category):
    db = getattr(g, 'db')
    data = {
        'result': {
            'variables': db.filter_variables_category(category),
        },
        'parameters': {
            'categories': category,
        },
        'meta': {
            'request_time': getattr(g, 'request_time')(),
        },
    }
    return data
