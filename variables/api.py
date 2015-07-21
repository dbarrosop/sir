from flask import g
import helpers.api


def _variables_post(request):
    # curl -i -H "Content-Type: application/json" -X POST -d '{"name": "test", "content": "this_is_a_test", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables
    db = getattr(g, 'db')

    name = request.json.get('name')
    content = request.json.get('content')
    category = request.json.get('category')
    extra_vars = request.json.get('extra_vars')

    db.put_variables(name, content, category, extra_vars)

    result = db.get_variable(category, name)
    parameters = {
        'name': name,
        'content': content,
        'category': category,
        'extra_vars': str(extra_vars),
    }
    return helpers.api.build_api_response(result, error=False, **parameters)


def _variables_get(request):
    db = getattr(g, 'db')
    result = db.get_variables()
    parameters = {}
    return helpers.api.build_api_response(result, error=False, **parameters)


def variables(request):
    if request.method == 'GET':
        return _variables_get(request)
    elif request.method == 'POST':
        return _variables_post(request)


def _api_variables_var_id_get(request, name):
    db = getattr(g, 'db')
    result = db.get_variable(name)
    parameters = {
        'name': name,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)


def api_variables_name(request, category, name):
    db = getattr(g, 'db')

    if request.method == 'GET':
        result = db.get_variable(category, name)
    elif request.method == 'PUT':
        # curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "test", "content": "this_is_a_testa", "category": "development", "extra_vars": {"ads": "qwe", "asd": "zxc"}}' http://127.0.0.1:5000/api/v1.0/variables/test
        variable = db.get_variable(category, name)[0]
        new_name = request.json.get('name', variable['name'])
        new_content = request.json.get('content', variable['content'])
        new_category = request.json.get('category', variable['category'])
        new_extra_vars = request.json.get('extra_vars', variable['extra_vars'])
        db.update_variable(name, category, new_name, new_content, new_category, new_extra_vars)
        result = db.get_variable(new_category, new_name)
    elif request.method == 'DELETE':
        db.delete_variable(category, name)
        result = []

    result = result
    parameters = {
        'name': name,
        'categories': category,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)


def variables_category(request):
    db = getattr(g, 'db')
    result = db.get_categories()
    parameters = {}
    return helpers.api.build_api_response(result, error=False, **parameters)


def variables_filter_by_category(request, category):
    db = getattr(g, 'db')
    result = db.filter_variables_category(category)
    parameters = {
        'categories': category,
    }
    return helpers.api.build_api_response(result, error=False, **parameters)
