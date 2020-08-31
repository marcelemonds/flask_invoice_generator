from flask import Flask, render_template, jsonify
from forms import PositionsForm, InvoiceForm
from decouple import config

def create_app():
    app = Flask(__name__)
    app.secret_key = config('SECRET_KEY', default='you-will-never-guess')


    @app.route('/')
    def index():

        return render_template(
            '/index.html',
            title='Invoice Generator',
            active_page='home'
        )


    @app.route('/invoice')
    def invoice_form():
        positions_form = PositionsForm(prefix='positions')
        invoice_form = InvoiceForm(prefix='invoice')

        return render_template(
            '/invoice_form.html',
            title='Invoice Form',
            active_page='form',
            positions_form=positions_form,
            invoice_form=invoice_form
        )


    return app