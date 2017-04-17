from flask_wtf import Form,FlaskForm
from wtforms import StringField, BooleanField,validators,TextField,DateField
from wtforms.validators import DataRequired, Optional

class searchFlight(Form):
    dep_place = StringField('Departure City', validators=[DataRequired()],render_kw={"placeholder": "Phuket"})
    dest_place = StringField('Destination City', validators=[DataRequired()],render_kw={"placeholder": "Melbourne"})
    dep_date=DateField('Departure Date', format='%d-%m-%Y',validators=[DataRequired()],render_kw={"placeholder": "1-1-2017"})
    dest_date=DateField('Return Date', format='%d-%m-%Y',validators=[Optional()],render_kw={"placeholder": "1-1-2017"})