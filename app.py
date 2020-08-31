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


    @app.route('/positions', methods=['POST'])
    def positions_add():
        positions_form = PositionsForm(prefix='positions')
        success = False
        data = {}
        if positions_form.validate_on_submit():
            data = {
                'unit': positions_form.unit.data,
                'amount': positions_form.amount.data,
                'price': positions_form.price.data,
                'description': positions_form.description.data
            }
            success = True

        body = {
            'success': success,
            'data': data
        }
        print(body)
        return jsonify(body), 200

    return app