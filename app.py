from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():

        return render_template(
            '/index.html',
            title='Invoice Generator',
            active_page='home'
        )

    @app.route('/invoice_form')
    def invoice_form():

        return render_template(
            '/invoice_form.html',
            title='Invoice Form',
            active_page='form'
        )

    return app