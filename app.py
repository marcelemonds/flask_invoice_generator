from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
from forms import PositionsForm, InvoiceForm
from helper import float_check
from decouple import config
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.secret_key = config('SECRET_KEY', default='you-will-never-guess')
    csrf = CSRFProtect(app)

    @app.route('/')
    def index():

        return render_template(
            '/index.html',
            title='Invoice Generator',
            active_page='home'
        )


    @app.route('/invoice_data', methods=['GET', 'POST'])
    def invoice_form():
        positions_form = PositionsForm(prefix='positions')
        invoice_form = InvoiceForm(prefix='invoice')

        if request.method == 'POST':
            if positions_form.validate_on_submit():
                data = {
                    'unit': positions_form.unit.data,
                    'amount': positions_form.amount.data,
                    'price': positions_form.price.data,
                    'description': positions_form.description.data
                }
                flash('Position succesfully added!', 'success')
                success = True
                print(data)
            else:
                flash('Please check your form input!', 'error')
            print(positions_form.errors)

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
        if positions_form.validate_on_submit():
            data = {
                'unit': positions_form.unit.data,
                'amount': positions_form.amount.data,
                'price': positions_form.price.data,
                'description': positions_form.description.data
            }
            flash('Position succesfully added!', 'success')
            success = True
            print(data)
        else:
            flash('Please check your form input!', 'error')
        print(positions_form.errors)
        # return redirect(url_for('invoice_form'))
        invoice_form = InvoiceForm(prefix='invoice')

        return render_template(
            '/invoice_form.html',
            title='Invoice Form',
            active_page='form',
            positions_form=positions_form,
            invoice_form=invoice_form
        )

    return app