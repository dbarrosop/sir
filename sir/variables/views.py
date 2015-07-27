from flask import render_template
from flask import g

def browse_variables(request):
    db = getattr(g, 'db', None)
    context = dict()

    context['categories'] = db.get_categories()

    context['filter_category'] = request.args.get('category', None)

    if context['filter_category'] is None:
        context['variables'] = db.get_variables()
    else:
        context['variables'] = db.filter_variables_category(context['filter_category'])
    return render_template('variables/browse.html', **context)

'''
def edit_variable(request, orig_category, orig_name):
    db = getattr(g, 'db', None)
    context = dict()
    context['saved'] = False
    context['deleted'] = False
    context['orig_category'] = orig_category
    context['orig_name'] = orig_name

    if request.method == 'GET':
        context['variable'] = db.get_variable(orig_category, orig_name)
    elif request.method == 'POST':
        category = request.form.get('category')
        name = request.form.get('name')
        content = request.form.get('content')
        extra_vars = request.form.get('extra_vars')
        db.update_variable(orig_name, orig_category, name, content, category, extra_vars)
        context['saved'] = True
        context['variable'] = db.get_variable(orig_category, orig_name)

    return render_template('variables/edit.html', **context)
'''
