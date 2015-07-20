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
