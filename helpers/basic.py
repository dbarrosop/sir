from flask import render_template


def start_page(g, request):
    return render_template('basic/start_page.html')
