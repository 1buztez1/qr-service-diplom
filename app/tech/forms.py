from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class AddDeviceForm(FlaskForm):
    tech_name = StringField('Название устройства', validators=[DataRequired(), Length(max=256)])
    description = TextAreaField('Описание', validators=[Length(max=500)])
    serial_number = StringField('Серийный номер', validators=[Length(max=128)])
    tech_group_id = SelectField('Группа устройств', coerce=int, validators=[DataRequired()])
    status_id = SelectField('Статус', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить устройство')