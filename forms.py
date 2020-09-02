from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError


def integer_check(form, field):
    if type(field.data) != int:
        raise ValidationError('Please insert a numeric value!')
    if field.data < 0:
        raise ValidationError('Please enter a positive value!')


def negativ_check(form, field):
    if field.data < 0:
        raise ValidationError('Please enter a positive value!')


class PositionsForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), negativ_check])
    unit = SelectField('Unit', choices=[('', '...'), ('Conversion', 'Conversion'), ('Hour', 'Hour')], validators=[DataRequired()])
    price = FloatField('Price/Unit', validators=[DataRequired(), negativ_check])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])


class InvoiceForm(FlaskForm):
    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])
    invoice_number = StringField('Invoice #', validators=[DataRequired()])
    company_name = StringField('Company', validators=[DataRequired()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_number = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired(), integer_check])
