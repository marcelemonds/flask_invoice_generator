from flask import\
    Flask,\
    render_template,\
    jsonify,\
    redirect,\
    url_for,\
    flash,\
    request,\
    send_file
from forms import PositionsForm, InvoiceForm
from models import setup_db, db_drop_and_create_all, Positions, InvoiceDetails
from filters import currencyFormat
from decouple import config
from weasyprint import HTML
import io
import datetime


def create_app():
    app = Flask(__name__)
    app.secret_key = config('SECRET_KEY', default='you-will-never-guess')
    app.jinja_env.filters['currencyFormat'] = currencyFormat
    setup_db(app)
    '''
    uncomment the following line to initialize the databse
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
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
        invoice_details = InvoiceDetails.query.one_or_none()
        positions_form = PositionsForm(prefix='positions')
        invoice_form = InvoiceForm(prefix='invoice', obj=invoice_details)

        if request.method == 'POST':
            if positions_form.validate_on_submit():
                unit = positions_form.unit.data
                amount = positions_form.amount.data
                price = positions_form.price.data
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
            elif invoice_form.validate_on_submit():
                form_invoice_details = invoice_form.data
                form_invoice_details.pop('csrf_token', None)
                if invoice_details is None:
                    invoice_details = InvoiceDetails(**form_invoice_details)
                    invoice_details.insert()
                else:
                    invoice_details.update(**form_invoice_details)

                positions = Positions.query.all()
                total = 0
                for position in positions:
                    total += position.total
                created = datetime.date.today()
                payment_due = created + datetime.timedelta(days=14)

                return render_template('/invoice_details.html',
                                       title='Invoice Details',
                                       invoice_details=invoice_details,
                                       positions=positions,
                                       created=created,
                                       payment_due=payment_due,
                                       total=total
                                       )
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

    @app.route('/position_delete', methods=['DELETE'])
    def position_delete():
        position_id = request.get_json()['position_id']
        url = url_for('invoice_form')
        try:
            position = Positions.query.get(position_id)
            position.delete()
            flash('Position successfully deleted.', 'success')
        except Exception as e:
            flash('Position could not be deleted.', 'error')
            flash(e, 'error')

        body = {
            'url': url
        }

        return jsonify(body), 200

    @app.route('/invoice_pdf', methods=['POST'])
    def invoice_pdf():
        invoice_details = InvoiceDetails.query.one_or_none()
        positions = Positions.query.all()
        total = 0
        for position in positions:
            total += position.total
        created = datetime.date.today()
        payment_due = created + datetime.timedelta(days=14)
        try:
            rendered = render_template('invoice_details_pdf.html',
                                       invoice_details=invoice_details,
                                       positions=positions,
                                       created=created,
                                       payment_due=payment_due,
                                       total=total
                                       )
            html = HTML(string=rendered)
            invoice_pdf = html.write_pdf()
            return send_file(
                io.BytesIO(invoice_pdf),
                attachment_filename=f'invoice_{invoice_details.invoice_number}.pdf'
                )
        except Exception as e:
            flash(
                'An error occored and the pdf invoice could not be created.',
                'error'
                )
            flash(e, 'error')

            return render_template('/invoice_details.html',
                                   title='Invoice Details',
                                   invoice_details=invoice_details,
                                   positions=positions,
                                   created=created,
                                   payment_due=payment_due,
                                   total=total
                                   )

    return app
