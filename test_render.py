from app import create_app
from flask import render_template

app = create_app('development')

with app.app_context():
    with app.test_request_context():
        print("Rendering dashboard with no data...")
        html = render_template('dashboard.html', tasks=[], goals=[])
        print(html[:500])
        print("...done")
