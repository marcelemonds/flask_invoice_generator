from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
from forms import PositionsForm, InvoiceForm
from models import setup_db, db_drop_and_create_all, Positions
from decouple import config
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.secret_key = config('SECRET_KEY', default='you-will-never-guess')
    csrf = CSRFProtect(app)
    setup_db(app)
    db_drop_and_create_all()

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
                unit = positions_form.unit.data
                amount = positions_form.amount.data
                price =  positions_form.price.data
                description = positions_form.description.data
                total = amount * price
                new_position = Positions(
                    unit=unit,
                    amount=amount,
                    price=price,
                    description=description,
                    total=total
                )
                new_position.insert()

                flash('Position succesfully added!', 'success')
                success = True
            else:
                flash('Please check your form input!', 'error')

        positions = Positions.query.all()

        return render_template(
            '/invoice_form.html',
            title='Invoice Form',
            active_page='form',
            positions_form=positions_form,
            invoice_form=invoice_form,
            positions=positions
        )

    return app