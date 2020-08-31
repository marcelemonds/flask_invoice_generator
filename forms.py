from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


def integer_check(form, field):
    if type(field.data) != int:
        raise ValidationError('Please insert a number!')


class PositionsForm(FlaskForm):
    amount = FloatField('Amount')
    unit = SelectField('Unit', choices=[('','...'),('Conversion','Conversion'),('Hour','Hour')])
    price = FloatField('Price/Unit')
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])


class InvoiceForm(FlaskForm):
    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('Ende', validators=[DataRequired()])
    company_name = StringField('Company')
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_number = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired(), integer_check])